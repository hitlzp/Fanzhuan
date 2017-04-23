# -*- coding: utf-8 -*-
from commonapp.views import logcheck
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import Context
from django.shortcuts import render_to_response
from django.http import JsonResponse
from commonapp.models import User_class, Students, Inclass
from teacherapp.models import Course_t, Segmnet_t, Table_t
import time
from django.db import transaction

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
            selectedcourse = Course_t.objects.filter(id = courseid)[0]#学生选择的一个课程
                  
    cdic = {"cname":selectedcourse.cname, "courserecommend":selectedcourse.recommend}
    return JsonResponse(cdic)

def Command(request):#学生端从数据库获取教师的命令
    command = []#本课程当前教师端发送来的命令
    segtime = []#存储各个环节所占时间
    segintroduce = []#环节的介绍
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            if Inclass.objects.filter(courseid_id = courseid):#判断当前课程是否正在上课，或即将上课
                thecourse = Inclass.objects.filter(courseid_id = courseid)[0]
                if thecourse.isvalue == 1:
                    command.append(thecourse.command)
                    command.append(thecourse.segment)    
            all_segment = Segmnet_t.objects.filter(tcourse_id = courseid)
            for segment in all_segment:
                segtime.append(segment.minute)
                segintroduce.append(segment.content)
    cdic = {"command":command, "segtime":segtime, "segintroduce":segintroduce}
    return JsonResponse(cdic) 

def GradeS(request):
    choice = [0]*5#存储需要的评分种类，学生共三种
    temp1 = []
    temp2 = []
    nameingroup = []
    idingroup = []
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('courseid')
            segment = request.POST.get('segment')
            thecourse = Course_t.objects.filter(id = courseid)[0]
            thesegment = Segmnet_t.objects.filter(tcourse_id = courseid)[int(segment) - 1]
            all_table = Table_t.objects.filter(tsegment_id = thesegment.id)
            for table in all_table:
                choice[table.choice -1] = table.ratio
            groupnum = thecourse.sum / thecourse.groupsum
            stuid = request.user.id
            stuname = User.objects.filter(id = stuid)[0].username
            mygroup = Students.objects.filter(stu_id = stuid, course_id = courseid)[0].group
            for i in range(1, groupnum + 1):
                groupstu = Students.objects.filter(group = i)
                for i in range(0, len(groupstu)):
                    temp1.append(groupstu[i].stu_id)
                    name = User.objects.filter(id = groupstu[i].stu_id)[0].username
                    temp2.append(name)
                idingroup.append(temp1)
                nameingroup.append(temp2)
                temp1 = []
                temp2 = []
            
    #groupnum  小组数量
    #choice 五种评分各占比例
    #stuid 自评学生id
    #stuname 自评学生姓名
    #mygroup 当前学生所在的小组号
    #idingroup保存小组成员id 以组为单位[[...], [...], [...]]
    #nameingroup保存小组成员姓名以组为单位[[...], [...], [...]]
    #thecourse.groupsum小组人数
    cdic = {"groupnum":groupnum, "choice":choice, "stuid":stuid, "stuname":stuname, "mygroup":mygroup, \
            "nameingroup":nameingroup, "idingroup":idingroup, "groupsum":thecourse.groupsum}
    return JsonResponse(cdic) 

def Savegrade(request):#从前端获取学生的评价信息
    stugrade = []#存放选择本课程的每位同学的成绩
    stugroup = []#存放选择本课程学生的小组号
    stuids = []#存放选择本课程学生的id
    groupid = [] #当前用户小组成员的id
    ratio = [0]*5#各个部分所占的比例
    if request.POST:
        if request.is_ajax():
            with transaction.atomic():#Django 的事务管理
                stuid = request.user.id
                groupofmine = request.POST.get('stugroup')
                courseid = request.POST.get('courseid')
                segment = request.POST.get('segment')
                groupsum = request.POST.get('groupsum')
                g2ggrade = request.POST.getlist('g2ggrade')
                giggrade = request.POST.getlist('giggrade')
                selfgrade = request.POST.getlist('selfgrade')
                
                allperson = Course_t.objects.filter(id = courseid)[0].sum
                ratios = Table_t.objects.filter(tsegment_id = int(segment))
                for aa in ratios:
                    ratio[int(aa.choice)-1] = int(aa.ratio)#select_for_update()为mysql数据库行锁
                hahh = Students.objects.select_for_update().filter(course_id = courseid, group = int(groupofmine))
                for theid in hahh:
                    groupid.append(theid.id)
                all_grade = Students.objects.select_for_update().filter(course_id = courseid)
                for grade in all_grade:
                    stugrade.append(grade.grade)
                    stugroup.append(grade.group)
                    stuids.append(grade.id)
                for i in range(0, len(all_grade)):#更新了组间评论成绩
                    for j in range(1, len(g2ggrade) + 1):
                        if(stugroup[i] == j):
                            stugrade[i] += int(g2ggrade[j]) * ratio[2] / (100.00 * allperson)                
                for w in range(0, len(all_grade)): #更新了组内评论成绩
                    for u in range(0, int(groupsum)):
                        if groupid[u] == all_grade[w].id:
                            stugrade[w] += int(giggrade[u+1]) * ratio[3] / (100.00 * int(groupsum))
                for k in range(0, len(stuids)):
                    Students.objects.filter(id = stuids[k]).update(
                                                                      grade = stugrade[k],\
                                                                      )
                    
                mypregrade = Students.objects.filter(course_id = courseid, stu_id = stuid)[0].grade#更新了自评成绩
                newgrade = mypregrade + int(selfgrade[0]) * ratio[4] / 100.00                                                   
                Students.objects.filter(course_id = courseid, stu_id = stuid).update(
                                                                      grade = newgrade,\
                                                                      ) 
                print "OK"
     
    return JsonResponse({"rr":1}) 