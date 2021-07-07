from graphql_auth.schema import MeQuery
import graphene
import graphene.relay as relay
from .types import  AllowAuthenticatedALUserType, AllowSelfALUserType
from ..utils import AllowAdministratorFilter


class UserQueries(MeQuery, graphene.ObjectType):
    users = AllowAdministratorFilter(AllowAuthenticatedALUserType)
    user =  relay.Node.Field(AllowAuthenticatedALUserType)
    me = graphene.Field(AllowSelfALUserType)

    def resolve_me(root, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
    