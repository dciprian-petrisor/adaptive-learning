# from adaptive_learning.schema.utils import AllowAdministrator
import graphene
from graphene_django.types import DjangoObjectType
from adaptive_learning.backend.models import ALUser
from graphene_permissions.mixins import AuthNode, AuthFilter


# class AllowAdministratorALUserType(AuthNode, DjangoObjectType):
#     permission_classes = (AllowAdministrator,)
#     class Meta:
#         model = ALUser
#         exclude = ('password', )
#         filter_fields = ["first_name", "last_name", "date_joined", "is_admin"]
#         interfaces = (graphene.relay.Node,)
#         skip_registry = True
