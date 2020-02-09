from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/regno/<filename>
    return '{0}/{1}'.format(instance.student.regno, filename)



class Department(models.Model):
    deptname = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.deptname

class Faculty(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userid)

class Student(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    regno = models.CharField(max_length=20,blank=False)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.CharField(max_length=20,blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.regno

class File(models.Model):
    title = models.CharField(max_length=20, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    path = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
