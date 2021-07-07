from graphql_relay.connection.arrayconnection import offset_to_cursor
from adaptive_learning.schema.user.types import AllowAuthenticatedALUserType
from adaptive_learning.schema.utils import AllowAuthenticatedFilter
import uuid
import graphene
import shortuuid
import os
from graphene_file_upload.scalars import Upload
from graphql_relay.node.node import from_global_id
from adaptive_learning.schema.classroom.types import AllowAuthenticatedClassRoomMembershipType, AllowAuthenticatedClassRoomType, AllowClassRoomMember, AllowClassRoomOwnerOrTeacher, ClassRoomPostCommentEdge, ClassRoomPostEdge
from graphene_permissions.mixins import AuthMutation
from graphene_permissions.permissions import AllowAuthenticated
from adaptive_learning.backend.models import ALUser, ClassRoom, ClassRoomMaterial, ClassRoomMembership, ClassRoomPost, ClassRoomPostComment, MATERIAL_TYPE_CHOICES, PrivateMedia
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from adaptive_learning.settings import FS_STORAGE_LOCATION, PRIVATE_MEDIA_PATH

fs = FileSystemStorage(location=FS_STORAGE_LOCATION)
MEMBER_TYPES_DICT = {v:k for k,v in ClassRoomMembership.MEMBER_TYPE_CHOICES}
MATERIAL_TYPES_DICT =  {v:k for k,v in MATERIAL_TYPE_CHOICES}

class UpdateUserMembershipType(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, AllowClassRoomOwnerOrTeacher )
    success = graphene.Boolean()
    message = graphene.String()
    updated_member = graphene.Field(AllowAuthenticatedALUserType)
    updated_membership = graphene.Field(AllowAuthenticatedClassRoomMembershipType._meta.fields['member_type']._type._of_type)
    class Input:
        id = graphene.String(required=True)
        user_id = graphene.String(required=True)
        new_membership_type = graphene.Field(AllowAuthenticatedClassRoomMembershipType._meta.fields['member_type']._type._of_type)
    
    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return UpdateUserMembershipType(success=False, updated_membership=None, updated_member=None, message="You do not have permission to perform this action.")
        
        if input['new_membership_type'] == MEMBER_TYPES_DICT['Owner']:
            return UpdateUserMembershipType(success=False, updated_membership=None, updated_member=None, message="Will not update membership type to Owner.")

        try:
            classroom: ClassRoom = ClassRoom.objects.get(pk=from_global_id(input['id'])[1])
        except ClassRoom.DoesNotExist:
            return UpdateUserMembershipType(success=False, updated_membership=None, updated_member=None, message="No classroom with the specified ID exists.")
        
        target = ALUser.objects.get(pk=from_global_id(input['user_id'])[1])
        target_membership = ClassRoomMembership.objects.filter(classroom=classroom, user=target).first()
        if not target_membership:
            return UpdateUserMembershipType(success=False, updated_membership=None, updated_member=None, message="No existing membership was found for the specified user.")
        
        target_membership.member_type = input['new_membership_type']
        target_membership.save()
        return UpdateUserMembershipType(success=True, updated_membership=target_membership.member_type, updated_member=target, message="User membership updated.")

class RemoveMemberFromClassRoomMutation(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, AllowClassRoomOwnerOrTeacher )
    success = graphene.Boolean()
    message = graphene.String()
    classroom_members = AllowAuthenticatedFilter(AllowAuthenticatedClassRoomMembershipType)
    class Input:
        id = graphene.String(required=True)
        user_id = graphene.String(required=True)
    
    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return RemoveMemberFromClassRoomMutation(success=False, classroom_members= None, message="You do not have permission to perform this action.")
        
        try:
            classroom: ClassRoom = ClassRoom.objects.get(pk=from_global_id(input['id'])[1])
        except ClassRoom.DoesNotExist:
            return RemoveMemberFromClassRoomMutation(success=False, classroom_members=None, message="No classroom with the specified ID exists.")
        
        target = ALUser.objects.get(pk=from_global_id(input['user_id'])[1])
       
        classroom.members.remove(target)
        memberships = ClassRoomMembership.objects.filter(classroom=classroom)
        return RemoveMemberFromClassRoomMutation(success=True, classroom_members=memberships, message="Member removed.")


class LeaveClassRoomMutation(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, )
    success = graphene.Boolean()
    message = graphene.String()

    class Input:
        id = graphene.String(required=True)
    
    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return LeaveClassRoomMutation(success=False, message="You do not have permission to perform this action.")
        
        try:
            classroom = ClassRoom.objects.get(pk=from_global_id(input['id'])[1])
        except ClassRoom.DoesNotExist:
            return LeaveClassRoomMutation(success=False, message="No classroom with the specified ID exists.")
        
        user: ALUser = info.context.user
        membership = classroom.members.filter(username=user.username).first()
        if not membership:
            return LeaveClassRoomMutation(success=False, message="You are not a member of this classroom.")
        
        classroom.members.remove(membership)

        # delete if no members left in classroom
        if not classroom.members:
            classroom.delete()
            
        return LeaveClassRoomMutation(success=True, message="You have left the classroom.")

class CreateClassRoomMutation(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, )
    success = graphene.Boolean()
    classroom = graphene.Field(AllowAuthenticatedClassRoomType)

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
    

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return CreateClassRoomMutation(classroom=None, success=False)
        
        user: ALUser = info.context.user
        uuid = shortuuid.uuid()
        classroom = ClassRoom.objects.create(name=input['name'], description=input['description'], access_code=uuid)
        membership = ClassRoomMembership(user=user, classroom=classroom, member_type=MEMBER_TYPES_DICT['Owner'])
        classroom.save()
        membership.save()
        classroom.members.add(user)
        return CreateClassRoomMutation(success=True, classroom=classroom)




class JoinClassRoomMutation(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, )
    success = graphene.Boolean()
    classroom = graphene.Field(AllowAuthenticatedClassRoomType)
    message = graphene.String()

    class Input:
        access_code = graphene.String(required=True)
    
    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return JoinClassRoomMutation(success=False, classroom=None, message="You do not have permissions to perform this action.")
        try:
            classroom = ClassRoom.objects.get(access_code=input['access_code'])
        except ClassRoom.DoesNotExist as e:
            return JoinClassRoomMutation(success=False, classroom=None, message="No classroom with this access code exists.")

        user: ALUser = info.context.user
        if classroom.members.filter(pk=user.pk).exists():
            return JoinClassRoomMutation(success=False, classroom=None, message="You are already a member of this classroom.")

        membership = ClassRoomMembership(user=user, classroom=classroom, member_type=MEMBER_TYPES_DICT["Student"])
        membership.save()
        classroom.members.add(user)

        return JoinClassRoomMutation(success=True, classroom=classroom, message="Classroom join successfully!")


class UploadClassRoomCoverPhoto(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, AllowClassRoomOwnerOrTeacher)
    success = graphene.Boolean()
    classroom = graphene.Field(AllowAuthenticatedClassRoomType)
    message = graphene.String()

    class Input:
        file = Upload(required=True)
        id = graphene.String(required=True)
    
    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return UploadClassRoomCoverPhoto(success=False, classroom=None, message="You do not have permissions to perform this action.")
        
        try:
            classroom: ClassRoom = ClassRoom.objects.get(pk=from_global_id(input['id'])[1])
        except ClassRoom.DoesNotExist:
            return UploadClassRoomCoverPhoto(success=False,classroom=None, message="No classroom with the specified ID exists.")
        file = input['file']
        name = uuid.uuid4().hex
        name = fs.save(name + os.path.splitext(file.name)[1], file)
        media = PrivateMedia(original_file_name=file.name, path=os.path.join(PRIVATE_MEDIA_PATH, name))
        media.save()
        classroom.cover_photo = media
        classroom.save()
        return UploadClassRoomCoverPhoto(success=True, classroom=classroom, message="Cover photo uploaded successfully.")


class CreateClassRoomPostMutation(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, AllowClassRoomMember)
    success = graphene.Boolean()
    message = graphene.String()
    post = graphene.Field(ClassRoomPostEdge)


    class Input:
        mime_types = graphene.List(graphene.String)
        material_types = graphene.List(graphene.String)
        files = graphene.List(Upload)
        datetime = graphene.DateTime(required=True)
        text = graphene.String(required=True)
        classroom_id = graphene.String(required=True)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return CreateClassRoomPostMutation(success=False, post=None, message="You do not have permissions to perform this action.")
        user: ALUser = info.context.user
        
        try:
            classroom: ClassRoom = ClassRoom.objects.get(pk=from_global_id(input['classroom_id'])[1])
        except ClassRoom.DoesNotExist:
            return CreateClassRoomPostMutation(success=False, post=None, message="No classroom with the specified ID exists.")
        

        post = ClassRoomPost.objects.create(datetime=input['datetime'], author=user, text=input['text'], classroom = classroom)
        
        files = input['files']
        material_types = input['material_types']
        mime_types = input['mime_types']
        for file, material_type, mime_type in zip(files, material_types, mime_types):
            name = uuid.uuid4().hex
            name = fs.save(name + os.path.splitext(file.name)[1], file)
            m_type = MATERIAL_TYPES_DICT[material_type]
            material = ClassRoomMaterial(mime_type=mime_type, material_type=m_type, datetime=input['datetime'], author=user, classroom=classroom, original_file_name=file.name, path=os.path.join(PRIVATE_MEDIA_PATH, name))
            material.save()

            media = PrivateMedia(original_file_name=file.name, path=os.path.join(PRIVATE_MEDIA_PATH, name))
            media.post = post
            media.save()
        
        
        return CreateClassRoomPostMutation(success=True, post = ClassRoomPostEdge(cursor=offset_to_cursor(0), node=post), message="Post created.")

class CreateClassRoomPostCommentMutation(AuthMutation, graphene.ClientIDMutation):
    permission_classes = (AllowAuthenticated, AllowClassRoomMember)
    success = graphene.Boolean()
    comment = graphene.Field(ClassRoomPostCommentEdge)
    message = graphene.String()
    
    class Input:
        datetime = graphene.DateTime(required=True)
        text = graphene.String(required=True)
        post_id = graphene.String(required=True)
        
    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **input):
        if not cls.has_permission(root, info, input):
            return CreateClassRoomPostCommentMutation(success=False, comment=None, message="You do not have permissions to perform this action.")
        user: ALUser = info.context.user
        try:
            post: ClassRoomPost = ClassRoomPost.objects.get(pk=from_global_id(input['post_id'])[1])
        except ClassRoomPost.DoesNotExist:
            return CreateClassRoomPostCommentMutation(success=False, comment=None, message="No post with the specified ID exists.")
        
        comment = ClassRoomPostComment.objects.create(author=user, datetime=input['datetime'], text=input['text'], post=post)
        return CreateClassRoomPostCommentMutation(success=True, comment=ClassRoomPostCommentEdge(cursor=offset_to_cursor(0), node=comment), message="Comment created.")
 


class ClassRoomMutations(graphene.ObjectType):
    create_classroom = CreateClassRoomMutation.Field()
    join_classroom = JoinClassRoomMutation.Field()
    leave_classroom = LeaveClassRoomMutation.Field()
    upload_classroom_cover_photo = UploadClassRoomCoverPhoto.Field()
    remove_member_from_classroom = RemoveMemberFromClassRoomMutation.Field()
    update_user_membership_type = UpdateUserMembershipType.Field()
    create_classroom_post = CreateClassRoomPostMutation.Field()
    create_classroom_post_comment = CreateClassRoomPostCommentMutation.Field()
    pass