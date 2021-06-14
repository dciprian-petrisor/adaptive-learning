from graphene_django.filter.fields import DjangoFilterConnectionField
from adaptive_learning.backend.models import ClassRoom
from graphene_django.types import DjangoObjectType
from graphql_auth.schema import MeQuery
import graphene
import graphene.relay as relay
# from .types import  AllowAdministratorALUserType
from ..utils import AllowAdministratorFilter



class ClassRoomType(DjangoObjectType):
    class Meta:
        model = ClassRoom
        filter_fields = '__all__'
        fields = '__all__'
        interfaces = (relay.Node, )


class UserQueries(MeQuery, graphene.ObjectType):
    all_classrooms = DjangoFilterConnectionField(ClassRoomType)
    # users = AllowAdministratorFilter(AllowAdministratorALUserType)
    # user =  relay.Node.Field(AllowAdministratorALUserType)
    pass
    