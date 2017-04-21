# -*- coding: utf-8 -*-

from django.shortcuts import render
from commonapp.views import logcheck
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import render_to_response
from django.http import JsonResponse
from commonapp.models import User_class, Students
from teacherapp.models import Course_t
import time
# Create your views here.
def logcheck_s(request):#检测学生登陆情况
    test = request.user.id
    if not test:
        return 0
    elif not logcheck(request) == 0:
        return 0
    else:
        return 1
    
def login_s(request):#学生登陆
    test = request.user.id
    if test and logcheck(request) == 0:
        return HttpResponseRedirect("/student/main/")
    request.session.set_test_cookie()
    c = ({})
    if request.POST:
        post = request.POST
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            username = post["user"]
            password = post["pass"]
            user = User.objects.filter(username = post["user"])
            if not user:
                c = Context({"errors":"Invalid Username!"})
            else:
                imp_user = User_class.objects.filter(person__exact = user)
                if not imp_user.values()[0]['clas'] == 0:
                    c = Context({"errors":"Invalid Username!"})
                else:
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            auth.login(request, user)
                            c = Context({"username":username})
                            return HttpResponseRedirect("/student/main/")
                    else:
                        c = Context({"errors":"Invalid Password!"})
        else:
            c = Context({"errors":"Log in Failed!\nPlease enable cookies and try again."})
    return render_to_response("prj_login_student.html", c)


def reg_s(request):#学生注册
    errors = []
    if request.POST:
        post = request.POST
        for i in post.keys():
            if post[i] == "":
                errors.append("Please input " + i)
        if post["pass"] != post["re_pass"]:
            errors.append("Password doesn\'t match")
            c = Context({"errors":"Password doesn\'t match"})
        user = User.objects.filter(username = post["user"])
        if errors == []:
            if user:
                return render_to_response("prj_reg.html", {'errors': "User exists!"})
            new_user = User.objects.create_user( \
                                    username = post["user"], \
                                    password = post["pass"], \
                                    email = post["email"], \
                                    )
            add = User_class(person_id = new_user.id, clas = 0 )
            add.save()
            new_user.save()
            return HttpResponseRedirect("/student/")
    return render_to_response("prj_reg.html", {'errors': errors, })

def studentmain(request):#学生首页
    if logcheck_s(request) == 0:
        return HttpResponseRedirect("/student/")
    student= User.objects.filter(id = request.user.id)
    return render_to_response("student_main.html",{'student':student[0]})

def Mycourse(request):
    temp = []#存储学生选修过的课程的id
    temp2 = []
    mycourse = []#存储该学生所选择的课程的全部信息
    stuid = request.user.id
    stucourse = Students.objects.filter(stu_id = stuid)#获取当前用户参加课程的id
    for selectedcourse in stucourse:
        temp.append(selectedcourse.course_id)
        mycourse.append(Course_t.objects.filter(id = selectedcourse.course_id)[0])
    time.localtime(time.time())
    thedatetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#获取当前时间
    all_objects = Course_t.objects.all()
    for course in all_objects:
        all_students = Students.objects.filter(course_id = course.id)
        if len(all_students) < course.sum and str(course.starttime) > thedatetime and  (course.id not in temp):
            #判断筛选出那些未选满，开课时间晚于当前日期并且该学生未选修的课程
            temp2.append(course.id)
    check_box_list = request.GET.getlist('removecourse')
    for j in  check_box_list:
        Students.objects.filter(course_id = j, stu_id = stuid).delete()
    if not len(check_box_list) == 0:#删除后刷新当前网页
        return HttpResponseRedirect("/student/mycourse/")
    cdic = {"coursenum":temp2,"mycourse":mycourse}
    return render_to_response("mycourse.html", cdic)

def Mycourseajax(request):
    temp = []#存储学生选修过的课程的id
    temp2= []
    allcourse = []
    if request.POST:
        if request.is_ajax():
            stuid = request.user.id
            stucourse = Students.objects.filter(stu_id = stuid)#获取当前用户参加课程的id
            for selectedcourse in stucourse:
                temp.append(selectedcourse.course_id)
            time.localtime(time.time())
            thedatetime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#获取当前时间
            all_objects = Course_t.objects.all()
            for course in all_objects:
                all_students = Students.objects.filter(course_id = course.id)
                if len(all_students) < course.sum and str(course.starttime) > thedatetime and  (course.id not in temp):
                    #判断筛选出那些未选满，开课时间晚于当前日期并且该学生未选修的课程
                    theteacher = User.objects.filter(id = course.teacher_id)
                    temp2.append(course.id)
                    temp2.append(course.cname)
                    temp2.append(len(all_students))
                    temp2.append(course.sum)
                    temp2.append(theteacher[0].username)
                    temp2.append(course.starttime)
                    allcourse.append(temp2)
                    temp2 = []
    thedic = {"allcourse":allcourse, "yy":len(allcourse)}
    return JsonResponse(thedic)
    
def Addcourse(request):#学生点击课程名实现添加课程
    if request.POST:
        if request.is_ajax():
            addit = Students(course_id = request.POST.get('id'),\
                                  stu_id = request.user.id,\
                                  group = 0,\
                                  grade = 0,\
                                  )
            addit.save()
    return JsonResponse({"ff":1})

def Coursemessage(request):#点击课程显示课程介绍
    if request.POST:
        if request.is_ajax():
            all_objects = Course_t.objects.filter(id = request.POST.get('id'))
            print request.POST.get('id')
    return JsonResponse({"mess":all_objects[0].recommend})

def Stuinclass(request):#学生进入课堂界面，mycourse为当前学生选修的课程
    stucourse = []
    stuid = request.user.id
    mycourses = Students.objects.filter(stu_id = stuid)
    for course in mycourses:
        thecourse = Course_t.objects.filter(id = course.course_id)[0]
        stucourse.append(thecourse)
    cdic = {"mycourse":stucourse}
    return render_to_response("stu_inclass.html", cdic)

def Stu_inclass(request):#学生选择即将参加的课程（课堂），返回课程的相关信息
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            print courseid
            selectedcourse = Course_t.objects.filter(id = courseid)[0]#学生选择的一个课程
    cdic = {"cname":selectedcourse.cname, "courserecommend":selectedcourse.recommend}
    return JsonResponse(cdic)