from django.contrib.auth.models import AbstractUser
from django.db import models

class ALUser(AbstractUser):
    icon = models.OneToOneField('PrivateMedia', on_delete=models.DO_NOTHING, null=True)
    requires_password_reset = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, verbose_name="is admin")

class ClassRoomMembership(models.Model):
    MEMBER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'owner')
    )
    user = models.ForeignKey('ALUser', on_delete=models.CASCADE)
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)
    member_type = models.PositiveSmallIntegerField(choices=MEMBER_TYPE_CHOICES, blank=False)
    

class ClassRoomPost(models.Model):
    title = models.CharField(blank=False, max_length=80, verbose_name="post title")
    datetime = models.DateTimeField(blank=False, verbose_name="post date and time")
    author = models.ForeignKey(ALUser, on_delete=models.CASCADE, verbose_name="post author")
    text = models.CharField(blank=False,  max_length=1000, verbose_name="post text")
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)

class ClassRoomPostComment(models.Model):
    author = models.ForeignKey(ALUser, on_delete=models.CASCADE, verbose_name="comment author")
    datetime = models.DateTimeField(blank=False, verbose_name="comment date and time")
    text = models.CharField(blank=False, max_length=1000, verbose_name="comment text")
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)

class ClassRoom(models.Model):
    name = models.CharField(blank=False, max_length=50, verbose_name="classroom name")
    access_code = models.CharField(primary_key=True, blank=False, max_length=50, verbose_name="access_code")
    description = models.CharField(blank=False, max_length=200, verbose_name="classroom description")
    members = models.ManyToManyField(ALUser, blank=False, through='ClassRoomMembership')


class PrivateMedia(models.Model):
    original_file_name = models.CharField(null=True, max_length=300, verbose_name="original file name")
    path = models.CharField(primary_key=True, blank=False, max_length=300, verbose_name="private media path")