# import graphene
# from graphene_django.types import DjangoObjectType
# from graphene_permissions.mixins import AuthNode
# from graphene_permissions.permissions import AllowAny, AllowAuthenticated
# from adaptive_learning.backend.models import  ClassRoom, ClassRoomMembership, ClassRoomPost, ClassRoomPostComment
# from django_filters import FilterSet

# class AllowClassRoomMember(AllowAny):

#     @staticmethod
#     def has_node_permission(info, id):
#         classroom = ClassRoom.objects.get(pk=id)
#         if not classroom:
#             return False
        
#         return classroom.members.filter(username=info.context.user.username).exists()

# class AllowMembershipOwner(AllowAny):

#     @staticmethod
#     def has_node_permission(info, id):
#         membership = ClassRoomMembership.objects.get(pk=id)

#         if not membership:
#             return False
        
#         return membership.user == info.context.user


# class ClassRoomMemberFilter(FilterSet):
#     class Meta:
#         model = ClassRoom
#         fields = '__all__'

#     @property
#     def qs(self):
#         return super().qs.filter(members__username=self.request.user.username)
        

# class AllowAuthenticatedClassRoomPostType(AuthNode, DjangoObjectType):
#     permission_classes = (AllowAuthenticated, )

#     class Meta:
#         model = ClassRoomPost
#         filter_fields = '__all__'
#         interfaces = (graphene.relay.Node, )
#         skip_registry = True

# class AllowAuthenticatedClassRoomPostCommentType(AuthNode, DjangoObjectType):
#     permission_classes = (AllowAuthenticated, )

#     class Meta:
#         model = ClassRoomPostComment
#         filter_fields = '__all__'
#         interfaces = (graphene.relay.Node, )
#         skip_registry = True





# class AllowAuthenticatedClassRoomMembershipType(AuthNode, DjangoObjectType):
#     permission_classes = (AllowAuthenticated,AllowMembershipOwner )

#     class Meta:
#         model = ClassRoomMembership
#         filter_fields = '__all__'
#         interfaces = (graphene.relay.Node, )
#         skip_registry = True



# class AllowAuthenticatedClassRoomType(AuthNode, DjangoObjectType):
#     permission_classes = (AllowAuthenticated, AllowClassRoomMember)

#     class Meta:
#         model = ClassRoom
#         filterset_class = ClassRoomMemberFilter
#         fields = '__all__'
#         interfaces = (graphene.relay.Node, )
#         skip_registry = True

