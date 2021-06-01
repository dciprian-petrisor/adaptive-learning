from django.contrib.auth.models import AbstractUser
from django.db import models


class ALUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher')
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0][0])
    requires_password_reset = models.BooleanField(default=False)


class ALAdminableUser(ALUser):
    is_admin = models.BooleanField(default=False, verbose_name="is admin")

class ALStudent(ALAdminableUser):
    classrooms = models.ManyToManyField('ClassRoom', blank=True)
    pass

class ALTeacher(ALAdminableUser):
    classrooms = models.ManyToManyField('ClassRoom', blank=True)


class ClassRoom(models.Model):
    name = models.CharField(blank=False, max_length=50, verbose_name="classroom name")