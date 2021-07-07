import graphene
import os
import uuid
from graphql_auth import mutations
from adaptive_learning.settings import FS_STORAGE_LOCATION
from adaptive_learning.backend.models import ALUser, PrivateMedia
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload
from django.core.files.storage import FileSystemStorage
from adaptive_learning import settings
from ..media.types import PrivateMediaType

fs = FileSystemStorage(location=FS_STORAGE_LOCATION)

class UpdateIconMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    icon = graphene.Field(PrivateMediaType, id =  graphene.String())

    @login_required
    def mutate(self, info, file):
        if not file:
            return UpdateIconMutation(success=False)

        user: ALUser = info.context.user
        name = uuid.uuid4().hex
        # fs.save might reassign if the name ever has a collision, however mathematically improbable due to nature of uuid, this will safeguard against that
        name = fs.save(name + os.path.splitext(file.name)[1], file)
        # create an entry for the new private media to the user
        media = PrivateMedia(original_file_name=file.name, path=os.path.join(settings.PRIVATE_MEDIA_PATH, name))
        media.save()
        user.icon = media
        # save the updated user
        user.save()
        return UpdateIconMutation(success=True, icon=user.icon)

class UserMutations(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
    update_icon = UpdateIconMutation.Field()