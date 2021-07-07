from graphene_permissions.mixins import AuthFilter
from graphene_permissions.permissions import AllowAny, AllowAuthenticated
from graphql_relay.node.node import from_global_id


class AllowSelf(AllowAny):
    """Permission to allow only the currently authenticated user to perform a node get.
    """
    @staticmethod
    def has_node_permission(info, id):
        user = info.context.user
        return user.is_authenticated and user.id == from_global_id('ALUserType', id)

class AllowAdministrator(AllowAny):
    """Permission to allow only administrators to perform a node get, mutate or filter
    """
    @staticmethod
    def has_node_permission(info, id):
        user = info.context.user
        return user.is_authenticated and user.is_admin

    @staticmethod
    def has_mutation_permission(root, info, input):
        user = info.context.user
        return user.is_authenticated and user.is_admin
            
    @staticmethod
    def has_filter_permission(info):
        user = info.context.user
        return user.is_authenticated and user.is_admin



class AllowAdministratorFilter(AuthFilter):
    """Generic filter that allows only administrators to use the query it is applied on.
    """

    permission_classes = (AllowAdministrator, )


class AllowAuthenticatedFilter(AuthFilter):
    """Generic filter that allows only authenticated users to use theq uery it is applied on.
    """
    
    permission_classes = (AllowAuthenticated, )