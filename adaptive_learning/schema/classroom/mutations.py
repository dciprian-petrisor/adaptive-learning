# from adaptive_learning.schema.classroom.types import AllowAuthenticatedClassRoomType
# from graphene_permissions.mixins import AuthMutation
# from graphene_permissions.permissions import AllowAuthenticated
# from adaptive_learning.backend.models import ALUser, ClassRoom, ClassRoomMembership, ClassRoomPost, ClassRoomPostComment
import graphene
# import shortuuid

from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location="/app/uploads")
# MEMBER_TYPES_DICT = {v:k for k,v in ClassRoomMembership.MEMBER_TYPE_CHOICES}


# class CreateClassRoomMutation(AuthMutation, graphene.ClientIDMutation):
#     permission_classes = (AllowAuthenticated, )
#     success = graphene.Boolean()
#     classroom = graphene.Field(AllowAuthenticatedClassRoomType)

#     class Input:
#         name = graphene.String(required=True)
#         description = graphene.String(required=True)
    

#     @classmethod
#     def mutate_and_get_payload(cls, root, info, **input):
#         if not cls.has_permission(root, info, input):
#             return CreateClassRoomMutation(classroom=None, success=False)
        
#         user: ALUser = info.context.user
#         uuid = shortuuid.uuid()
#         classroom = ClassRoom.objects.create(name=input['name'], description=input['description'], access_code=uuid)
#         membership = ClassRoomMembership(user=user, classroom=classroom, member_type=MEMBER_TYPES_DICT['owner'])
#         classroom.save()
#         membership.save()
#         classroom.members.add(user)
#         return CreateClassRoomMutation(success=True, classroom=classroom)


# class JoinClassRoomMutation(AuthMutation, graphene.ClientIDMutation):
#     permission_classes = (AllowAuthenticated, )
#     success = graphene.Boolean()
#     classroom = graphene.Field(AllowAuthenticatedClassRoomType)
#     message = graphene.String()

#     class Input:
#         access_code = graphene.String(required=True)
    
#     @classmethod
#     def mutate_and_get_payload(cls, root, info, **input):
#         if not cls.has_permission(root, info, input):
#             return JoinClassRoomMutation(success=False, classroom=None, message="You do not have permissions to perform this action.")

#         classroom = ClassRoom.objects.get(access_code=input['access_code'])

#         if not classroom:
#             return JoinClassRoomMutation(success=False, classroom=None, message="No classroom with this access code exists.")

#         user: ALUser = info.context.user
#         if classroom.members.filter(pk=user.pk).exists():
#             return JoinClassRoomMutation(success=False, classroom=None, message="You are already a member of this classroom.")

#         membership = ClassRoomMembership(user=user, classroom=classroom, member_type=MEMBER_TYPES_DICT["student"])
#         membership.save()
#         classroom.members.add(user)

#         return JoinClassRoomMutation(success=True, classroom=classroom, message="Classroom join successfully!")


# class CreateClassRoomPostMutation(graphene.Mutation):
#     class Arguments:
#         title = graphene.String(required=True)
#         datetime = graphene.DateTime(required=True)
#         text = graphene.String(required=True)
#         classroom_id = graphene.String(required=True)
    
#     success = graphene.Boolean()
#     post = graphene.Field(ClassRoomPostType)
    
#     @login_required
#     def mutate(self, info, title, datetime, text, classroom_id):
#         user: ALUser = info.context.user
#         classroom = ClassRoom.objects.get(pk=classroom_id)
#         if not classroom:
#             raise ValueError("Invalid classroom id.")
        
#         post = ClassRoomPost.objects.create(title=title, datetime=datetime, author=user, text=text, classroom = classroom)

#         return CreateClassRoomMutation(success=True, post=post)

# class CreateClassRoomPostCommentMutation(graphene.Mutation):
#     class Arguments:
#         datetime = graphene.DateTime(required=True)
#         text = graphene.String(required=True)
#         classroom_id = graphene.String(required=True)
        
#     success = graphene.Boolean()
#     comment = graphene.Field(ClassRoomPostCommentType)

#     @login_required
#     def mutate(self, info, datetime, text, classroom_id):
#         user: ALUser = info.context.user
#         classroom = ClassRoom.objects.get(pk=classroom_id)
#         if not classroom:
#             raise ValueError("Invalid classroom id.")
        
#         comment = ClassRoomPostComment.objects.create(author=user, datetime=datetime, text=text, classroom=classroom)
#         return CreateClassRoomPostCommentMutation(success=True, comment=comment)



class ClassRoomMutations(graphene.ObjectType):
    # create_classroom = CreateClassRoomMutation.Field()
    # join_classroom = JoinClassRoomMutation.Field()
    # create_classroom_post = CreateClassRoomPostMutation.Field()
    # create_classroom_post_comment = CreateClassRoomPostCommentMutation.Field()
    pass