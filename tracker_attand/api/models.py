import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from tracker_attand import settings



class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    name = models.CharField(max_length=40, null=True)
    roll_no = models.CharField(max_length=40, null=True)
    course = models.CharField(max_length=40, null=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
@receiver(post_save,sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created= False, **kwargs):
    if created:
        Token.objects.create(user=instance)
class Course(models.Model):
    course_name = models.CharField(max_length = 40)

class Classname(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_name = models.CharField(max_length = 40)


class TeacherCreateHour(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classname, on_delete=models.CASCADE)
    time = models.DateTimeField()
    hour = models.CharField(max_length = 40)

    
class TeacherScanPost(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classname, on_delete=models.CASCADE)
    hour_id = models.ForeignKey(TeacherCreateHour, on_delete=models.CASCADE)
    special_uid = models.CharField(max_length = 40)

class AttendanceList(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classname, on_delete=models.CASCADE)
    hour_id = models.ForeignKey(TeacherCreateHour, on_delete=models.CASCADE)
    date = models.DateField()
    uid = models.CharField(max_length = 40)
    name = models.CharField(max_length = 30)

    
    def __str__(self):
        return self.uid