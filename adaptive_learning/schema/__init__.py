import graphene
from graphene_permissions.mixins import AuthFilter
from graphql_auth.schema import MeQuery, UserQuery

from .classroom.queries import ClassroomQueries
from .classroom.mutations import ClassRoomMutations
from.user.queries import UserQueries
from .user.mutations import UserMutations



class Query(UserQueries, graphene.ObjectType):
    pass
    

class Mutation(UserMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
