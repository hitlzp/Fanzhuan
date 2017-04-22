"""Fanzhuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from commonapp.views import menu,logout, forgot
from teacherapp.views import login_t,reg_t, coursemanage, addcourse, editcourse, editcourse_ajax, teachermain,\
ajax_course, addsegment, ajax_segment, addfinally, ajax_finally,inclassajax, inclass, startcourse,nextsegment,\
Fenzu, Randstu, Randgroup, GfromT, Grade_t, CommandT


from studentapp.views import login_s, reg_s, studentmain, Mycourse, Mycourseajax, Addcourse, Coursemessage, Stuinclass,\
Stu_inclass, Command, GradeS, Savegrade

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',menu),
    url(r'^teacher/$', login_t),
    url(r'^teacher/reg/$', reg_t),
    url(r'^logout/$', logout),
    url(r'^forgot/$', forgot), 
    url(r'^teacher/coursemanage/$', coursemanage),
    url(r'^teacher/addcourse/$', addcourse),
    url(r'^teacher/course/mycourse/$', editcourse),
    url(r'^teacher/course/mycourse/ajax/$', editcourse_ajax),
    url(r'^teacher/main/$', teachermain),
    url(r'^test/$', ajax_course),
    url(r'^teacher/addcourse/addsegment/$', addsegment),
    url(r'^test2/$', ajax_segment),
    url(r'^teacher/addcourse/finally/$', addfinally),
    url(r'^test3/$',ajax_finally),
    url(r'^teacher/class/$', inclass),
    url(r'^teacher/classajax/$', inclassajax),
    url(r'^teacher/startcourse/$', startcourse),
    url(r'^teacher/nextsegment/$', nextsegment),
    url(r'^teacher/fenzu/$', Fenzu),
    url(r'^teacher/randstu/$', Randstu),
    url(r'^teacher/randgroup/$', Randgroup),
    url(r'^teacher/gradeteacher/$', Grade_t),
    url(r'^teacher/gradefromteacher/$', GfromT),
    url(r'^student/$', login_s),
    url(r'^student/reg/$', reg_s),
    url(r'^student/main/$', studentmain),
    url(r'^student/mycourse/$', Mycourse),
    url(r'^student/mycourseajax/$', Mycourseajax),
    url(r'^student/addcourse/$', Addcourse),
    url(r'^student/coursemessage/$', Coursemessage),
    url(r'^student/inclass/$', Stuinclass),
    url(r'^student/stuinclassajax/$', Stu_inclass),
    url(r'^student/command/$', Command),
    url(r'^teacher/command/$', CommandT),
    url(r'^student/grades/$', GradeS),
    url(r'^student/savegrade/$', Savegrade),
]