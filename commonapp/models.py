# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teacherapp.models import Course_t
 
class User_class(models.Model):
    person = models.ForeignKey(User)
    clas = models.IntegerField(default=0)
    
class Students(models.Model):
    stu = models.ForeignKey(User)
    course = models.ForeignKey(Course_t)
    group = models.IntegerField(default=0)
    grade = models.FloatField(default=0)
    
class Inclass(models.Model):#课堂中教师控制学生端
    courseid = models.ForeignKey(Course_t)
    command = models.CharField(max_length=100)
    segment  = models.IntegerField(default=0)
    isvalue = models.IntegerField(default=0)
    
class Stumess(models.Model):
    courseid = models.ForeignKey(Course_t)
    stuname = models.CharField(max_length=100)
    question = models.TextField()
