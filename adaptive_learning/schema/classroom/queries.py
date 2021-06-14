from graphene_django.types import DjangoObjectType
from adaptive_learning.backend.models import ClassRoom
import graphene
from graphene import relay
# from .types import  AllowAuthenticatedClassRoomType, AllowAuthenticatedClassRoomMembershipType, ClassRoomType
# from ..utils import AllowAuthenticatedFilter

# class ClassRoomType(DjangoObjectType):
#     class Meta:
#         model = ClassRoom
#         fields = '__all__'
         
class ClassroomQueries(graphene.ObjectType):
    # classrooms = AllowAuthenticatedFilter(AllowAuthenticatedClassRoomType)
    # classroom = relay.Node.Field(AllowAuthenticatedClassRoomType)
    # membership = relay.Node.Field(AllowAuthenticatedClassRoomMembershipType)


    pass