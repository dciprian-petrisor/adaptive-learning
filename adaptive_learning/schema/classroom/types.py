from django_filters.filters import OrderingFilter
from graphene_django.fields import DjangoConnectionField
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphql_relay.connection.arrayconnection import cursor_to_offset
from graphql_relay.node.node import  from_global_id, to_global_id
import graphene
from graphene_django.types import DjangoObjectType
from graphene_permissions.mixins import AuthNode
from graphene_permissions.permissions import AllowAny, AllowAuthenticated
from adaptive_learning.backend.models import  ClassRoom, ClassRoomMaterial, ClassRoomMembership, ClassRoomPost, ClassRoomPostComment
from django_filters import FilterSet

MEMBER_TYPES_DICT = {v:k for k,v in ClassRoomMembership.MEMBER_TYPE_CHOICES}


class ClassRoomPostFilter(FilterSet):
    class Meta:
        model = ClassRoomPost
        fields = '__all__'
    order_by = OrderingFilter(fields=('datetime',))


class ClassRoomPostCommentFilter(FilterSet):
    class Meta:
        model = ClassRoomPostComment
        fields = '__all__'
    
    order_by = OrderingFilter(fields=('datetime', ))

class ClassRoomMaterialFilter(FilterSet):
    class Meta:
        model = ClassRoomMaterial
        fields = '__all__'

    order_by = OrderingFilter(fields=('datetime', ))

class AllowClassRoomOwnerOrTeacher(AllowAny):

    @staticmethod
    def has_node_permission(info, id):
        try:
            classroom_id = from_global_id(id)[1]
            classroom = ClassRoom.objects.get(pk=classroom_id)
            membership = info.context.user.classroom_memberships.filter(classroom=classroom).first()
            return membership and \
                 (membership.member_type == MEMBER_TYPES_DICT.get('Owner', None) or membership.member_type == MEMBER_TYPES_DICT.get('Teacher', None))
        except ClassRoom.DoesNotExist:
                return False

    @staticmethod
    def has_mutation_permission(root, info, input):
        try:
            classroom_id = from_global_id(input['id'])[1]
            classroom = ClassRoom.objects.get(pk=classroom_id)
            membership = info.context.user.classroom_memberships.filter(classroom=classroom).first()
            return membership and \
                 (membership.member_type == MEMBER_TYPES_DICT.get('Owner', None) or membership.member_type == MEMBER_TYPES_DICT.get('Teacher', None))
        except ClassRoom.DoesNotExist:
                return False



class AllowClassRoomMember(AllowAny):

    @staticmethod
    def has_node_permission(info, id):
        try:
            classroom = ClassRoom.objects.get(pk=id)
            return classroom.members.filter(username=info.context.user.username).exists()
        except ClassRoom.DoesNotExist:
                return False
        

class ClassRoomMemberFilter(FilterSet):
    class Meta:
        model = ClassRoom
        fields = '__all__'

    @property
    def qs(self):
        return super().qs.filter(members__username=self.request.user.username)
        

class AllowAuthenticatedClassRoomMembershipType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, )

    class Meta:
        name = "ClassRoomMembershipType"
        model = ClassRoomMembership
        filter_fields = '__all__'
        fields = '__all__'
        interfaces = (graphene.relay.Node, )


class AllowAuthenticatedClassRoomPostCommentType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, AllowClassRoomMember)

    class Meta:
        name = "ClassRoomPostCommentType"
        model = ClassRoomPostComment
        filter_fields = '__all__'
        fields = '__all__'
        interfaces = (graphene.relay.Node, )

class AllowAuthenticatedClassRoomMaterialType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, AllowClassRoomMember)

    class Meta:
        name = "ClassRoomMaterialType"
        model = ClassRoomMaterial
        fields = '__all__'
        interfaces = (graphene.relay.Node, )
    

class AllowAuthenticatedClassRoomPostType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, AllowClassRoomMember)

    class Meta:
        name = "ClassRoomPostType"
        model = ClassRoomPost
        fields = '__all__'
        interfaces = (graphene.relay.Node, )
    
    has_attachments = graphene.Boolean()
    def resolve_has_attachments(self, info):
        print(self.post_attachments, flush=True)
        return self.post_attachments.count() > 0

    

class AllowAuthenticatedClassRoomType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, AllowClassRoomMember)
    class Meta:
        name = 'ClassRoomType'
        model = ClassRoom
        filterset_class = ClassRoomMemberFilter
        fields = ('name', 'description', 'classroom_members', 'id', 'cover_photo', 'classroom_materials')
        interfaces = (graphene.relay.Node, )
    
    access_code = graphene.String()
    my_membership = graphene.Field(AllowAuthenticatedClassRoomMembershipType)
    classroom_posts = DjangoFilterConnectionField(AllowAuthenticatedClassRoomPostType, filterset_class=ClassRoomPostFilter)
    
    def resolve_access_code(self, info):
        membership = self.classroom_members.filter(user=info.context.user).first()
        if membership.member_type == 'owner' or membership.member_type == 'teacher':
            return self.access_code
        return None
    
    def resolve_my_membership(self, info):
        membership = self.classroom_members.filter(user=info.context.user).first()
        return membership

    def resolve_classroom_posts(self, info, **kwargs):
        return ClassRoomPostFilter(kwargs).qs.filter(classroom=self)
    
ClassRoomPostEdge = AllowAuthenticatedClassRoomPostType._meta.connection.Edge
ClassRoomPostCommentEdge = AllowAuthenticatedClassRoomPostCommentType._meta.connection.Edge