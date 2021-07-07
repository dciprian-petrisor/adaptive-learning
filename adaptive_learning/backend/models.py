from django.contrib.auth.models import AbstractUser
from django.db import models

MATERIAL_TYPE_CHOICES = (
        ('visual', 'Visual'),
        ('verbal', 'Verbal')
)
class ALUser(AbstractUser):
    icon = models.OneToOneField('PrivateMedia', on_delete=models.DO_NOTHING, null=True)
    requires_password_reset = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, verbose_name="is admin")
    has_completed_quiz = models.BooleanField(default=False, verbose_name="has completed quiz")
    learning_material_preference = models.CharField(max_length=100, choices=MATERIAL_TYPE_CHOICES, blank=False, default='visual')

class ClassRoomMembership(models.Model):
    MEMBER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('owner', 'Owner')
    )
    user = models.ForeignKey('ALUser', on_delete=models.CASCADE, related_name="classroom_memberships")
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE, related_name="classroom_members")
    member_type = models.CharField(max_length=100, choices=MEMBER_TYPE_CHOICES, blank=False)
    

class ClassRoomMaterial(models.Model):
    mime_type = models.CharField(max_length=300, verbose_name="mime type")
    material_type = models.CharField(max_length=100, choices=MATERIAL_TYPE_CHOICES, blank=False)
    datetime = models.DateTimeField(blank=False, verbose_name="material date and time")
    author = models.ForeignKey(ALUser, on_delete=models.CASCADE, verbose_name="material author", related_name="materials")
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE, related_name="classroom_materials")
    original_file_name = models.CharField(null=True, max_length=300, verbose_name="original file name")
    path = models.CharField(primary_key=True, blank=False, max_length=300, verbose_name="material path")

class ClassRoomPost(models.Model):
    datetime = models.DateTimeField(blank=False, verbose_name="post date and time")
    author = models.ForeignKey(ALUser, on_delete=models.CASCADE, verbose_name="post author", related_name="posts")
    text = models.CharField(blank=False,  max_length=1000, verbose_name="post text")
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE, related_name="classroom_posts")

class ClassRoomPostComment(models.Model):
    author = models.ForeignKey(ALUser, on_delete=models.CASCADE, verbose_name="comment author", related_name="post_comments")
    datetime = models.DateTimeField(blank=False, verbose_name="comment date and time")
    text = models.CharField(blank=False, max_length=1000, verbose_name="comment text")
    post = models.ForeignKey('ClassRoomPost', on_delete=models.CASCADE, related_name="post_comments")

class ClassRoom(models.Model):
    name = models.CharField(blank=False, max_length=50, verbose_name="classroom name")
    access_code = models.CharField(primary_key=True, blank=False, max_length=50, verbose_name="access_code")
    description = models.CharField(blank=False, max_length=200, verbose_name="classroom description")
    members = models.ManyToManyField(ALUser, blank=False, through='ClassRoomMembership', related_name="classrooms")
    cover_photo = models.OneToOneField('PrivateMedia', on_delete=models.CASCADE, null=True)


class PrivateMedia(models.Model):
    post = models.ForeignKey(ClassRoomPost, on_delete=models.CASCADE, blank=True, null=True, related_name="post_attachments")
    original_file_name = models.CharField(null=True, max_length=300, verbose_name="original file name")
    path = models.CharField(primary_key=True, blank=False, max_length=300, verbose_name="private media path")
