from adaptive_learning.backend.models import ALAdminableUser, ALUser
from graphql_auth.models import UserStatus
from django.db import migrations

def create_root_user(apps, schema_editor):
    admin_user = ALAdminableUser(email="root@gmail.com", first_name="Administrator", last_name="Administrator", username="root", is_staff=True, is_active=True, is_superuser=True, is_admin=True, requires_password_reset=True)
    admin_user.set_password("root")
    admin_user.save()
    user_status = UserStatus(archived=False, verified=True, user=admin_user)
    user_status.save()
   
class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
        ('graphql_auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_root_user)
    ]
