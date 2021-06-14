from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_root_user(apps, _):
    ALUser = apps.get_model('backend', 'ALUser')
    admin_user = ALUser.objects.create(email="root@gmail.com", first_name="Administrator", last_name="Administrator", username="root",
                                       is_staff=True, is_active=True, is_superuser=True, is_admin=True, requires_password_reset=True, password=make_password("root"))

    UserStatus = apps.get_model('graphql_auth', 'UserStatus')
    UserStatus.objects.create(archived=False, verified=True, user=admin_user)


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
        ('graphql_auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_root_user)
    ]
