# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from teacherapp.models import Course_t
 
class User_class(models.Model):
    person = models.ForeignKey(User)
    clas = models.IntegerField(default=0)
    
class Students(models.Model):
    stu = models.ForeignKey(User)
    course = models.ForeignKey(Course_t)
    group = models.IntegerField(default=0)
    grade = models.FloatField(default=0)