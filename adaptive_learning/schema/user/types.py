from adaptive_learning.schema.utils import AllowSelf
from graphene_permissions.permissions import AllowAuthenticated
import graphene
from graphene_django.types import DjangoObjectType
from adaptive_learning.backend.models import ALUser
from graphene_permissions.mixins import AuthNode


class AllowAuthenticatedALUserType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated,)
    class Meta:
        name = "ALUserType"
        model = ALUser
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'icon')
        filter_fields = ["id", "username", "first_name", "last_name", "date_joined"]
        interfaces = (graphene.relay.Node,)


class AllowSelfALUserType(AuthNode, DjangoObjectType):
    permission_classes = (AllowAuthenticated, AllowSelf )
    class Meta:
        model = ALUser
        exclude = ('password', 'classrooms')
        interfaces = (graphene.relay.Node,)
        skip_registry = True
    
    pk = graphene.Int()
    archived = graphene.Boolean()
    verified = graphene.Boolean()
    secondary_email = graphene.String()

    def resolve_pk(self, info):
        return self.pk

    def resolve_archived(self, info):
        return self.status.archived

    def resolve_verified(self, info):
        return self.status.verified

    def resolve_secondary_email(self, info):
        return self.status.secondary_email

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.select_related("status")