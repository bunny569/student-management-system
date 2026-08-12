from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here
class Course(models.Model):
    course=models.CharField(max_length=50)
    subject=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
      return self.course
    

class Student(models.Model):
    genders=[
        ("Male","male"),
        ("Female","female")
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=6,choices=genders,default="Male")
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    roll_number=models.CharField(max_length=20,unique=True)
    year=models.IntegerField(null=True,blank=True)
    address=models.TextField()
    admissiom_date=models.DateField()
    phone=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    genders=[
            ("Male","male"),
            ("Female","female")
        ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=100)
    teacher_id=models.CharField(max_length=10,unique=True)
    age=models.IntegerField()
    gender=models.CharField(max_length=6,choices=genders,default="Male")
    date_of_joining=models.DateField()
    department=models.ForeignKey(Course,max_length=30,on_delete=models.CASCADE,null=True,blank=True)
    phone=models.CharField(max_length=10)
    

    def __str__(self):
        return self.name

class attendence(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)
    year=models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    status=models.CharField(null=True,blank=True)
    def __str__(self):
        return self.student.roll_number
class notice(models.Model):
    title=models.CharField(max_length=300,null=True,blank=True)
    text=models.TextField()
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

