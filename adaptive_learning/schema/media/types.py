
from graphene_django.types import DjangoObjectType
from adaptive_learning.backend.models import PrivateMedia

class PrivateMediaType(DjangoObjectType):
    class Meta:
        model = PrivateMedia
        fields = '__all__'
