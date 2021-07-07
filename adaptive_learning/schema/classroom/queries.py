from graphql_relay.node.node import from_global_id
from adaptive_learning.backend.models import ClassRoom, ClassRoomPost
import graphene
from graphene import relay
from .types import AllowAuthenticatedClassRoomMaterialType, AllowAuthenticatedClassRoomPostCommentType, AllowAuthenticatedClassRoomPostType, AllowAuthenticatedClassRoomType, ClassRoomMaterialFilter,  ClassRoomPostCommentFilter
from ..utils import AllowAuthenticatedFilter
from graphql_jwt.decorators import login_required

class ClassroomQueries(graphene.ObjectType):
    my_classrooms = AllowAuthenticatedFilter(AllowAuthenticatedClassRoomType)
    classroom = relay.Node.Field(AllowAuthenticatedClassRoomType)
    post = relay.Node.Field(AllowAuthenticatedClassRoomPostType)
    classroom_materials = AllowAuthenticatedFilter(AllowAuthenticatedClassRoomMaterialType, classroom_id=graphene.ID(), filterset_class=ClassRoomMaterialFilter)
    comments = AllowAuthenticatedFilter(AllowAuthenticatedClassRoomPostCommentType, post_id=graphene.ID(), filterset_class=ClassRoomPostCommentFilter)

    
    @login_required
    def resolve_classroom_materials(root, info, classroom_id, **kwargs):
        _, id = from_global_id(classroom_id)
        classroom = ClassRoom.objects.get(pk=id)
        return ClassRoomMaterialFilter(kwargs).qs.filter(classroom=classroom)

    @login_required
    def resolve_comments(root, info, post_id, **kwargs):
        _, id = from_global_id(post_id)

        post = ClassRoomPost.objects.get(pk=id)
        return ClassRoomPostCommentFilter(kwargs).qs.filter(post=post)