# -*- coding: utf-8 -*-
from django.contrib import auth
from django.shortcuts import render
from commonapp.views import logcheck
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import Context, RequestContext
from commonapp.models import User_class, Students
from django.shortcuts import render_to_response
from teacherapp.models import Course_t, Segmnet_t, Table_t
from django.http import JsonResponse
import random
from random import choice

def logcheck_t(request):#检测教师登陆情况
    test = request.user.id
    if not test:
        return 0
    elif not logcheck(request) == 1:
        return 0
    else:
        return 1
# Create your views here.
def login_t(request):#教师登陆
    test = request.user.id
    if test and logcheck(request) == 1:
        return HttpResponseRedirect("/teacher/main/")
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
                if not imp_user.values()[0]['clas'] == 1:
                    c = Context({"errors":"Invalid Username!"})
                else:
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            auth.login(request, user)
                            c = Context({"username":username})
                            return HttpResponseRedirect("/teacher/main/")
                    else:
                        c = Context({"errors":"Invalid Password!"})
        else:
            c = Context({"errors":"Log in Failed!\nPlease enable cookies and try again."})
    return render_to_response("prj_login_teacher.html", c)

def clearcourse(request):#进入添加课程界面时自动清除无效课程
    test = request.user.id
    all_objects = Course_t.objects.filter(teacher_id = test)
    for i in range(len(all_objects)):   #删除无效数据
        if all_objects[i].isvalid == 0:
            Course_t.objects.filter(id = all_objects[i].id).delete()

def clearsegment(request):#进入编辑环节界面时自动清除无效环节
    test = request.user.id
    all_objects = Course_t.objects.filter(teacher_id = test)
    for i in range(len(all_objects)):   #删除无效数据
        if all_objects[i].isvalid == 0:
            all_objects2 = Segmnet_t.objects.filter(tcourse_id = all_objects[i])
            for j in range(len(all_objects2)): #删除无效数据
                if all_objects2[j].isvalid == 0:
                    Segmnet_t.objects.filter(id = all_objects2[j].id).delete()
                    
def reg_t(request):#教师注册
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
            add = User_class(person_id = new_user.id, clas = 1 )
            add.save()
            new_user.save()
            return HttpResponseRedirect("/teacher/")
    return render_to_response("prj_reg.html", {'errors': errors, })

def teachermain(request):#教师首页
    if logcheck_t(request) == 0:
        return HttpResponseRedirect("/teacher/")
    teacher = User.objects.filter(id = request.user.id)
    return render_to_response("teacher_main.html",{'teacher':teacher[0]})

def coursemanage(request):#进入课程管理界面
    all_objects2 = []
    if logcheck_t(request) == 0:
        return HttpResponseRedirect("/teacher/")
    test = request.user.id
    all_objects = Course_t.objects.filter(teacher_id = test)
    for i in range(len(all_objects)):
        if all_objects[i].isvalid == 1:
            all_objects2.append(all_objects[i])
    check_box_list = request.GET.getlist('deletecourse')
    for j in  check_box_list:
        Course_t.objects.filter(id = j).delete()
    if not len(check_box_list) == 0:
        return HttpResponseRedirect("/teacher/coursemanage/")
    return render_to_response("course_manage.html", {'all_objects':all_objects2})

def editcourse(request):#点击课程可以跳转到这个界面浏览自己的课程详细信息或修改课程
    cid = request.GET["id"]
    seg_dict = {}
    course = Course_t.objects.filter(id = cid)
    segment = course[0].segmentsum
    all_objects = Segmnet_t.objects.filter(tcourse_id = cid)
    for j in range(segment):
        seg_dict[j+1] = all_objects[j].ratio
        
    if request.POST:#修改后的数据进行提交
        post = request.POST
        check_box_list = request.POST.getlist("type")#更新课程
        Course_t.objects.filter(id=cid).update(cname = post["cname"],\
                                               sum = post["sum_s"],\
                                               groupsum = post["group"],\
                                               recommend = post["introduce_c"],\
                                               mytype = int(check_box_list[0]),\
                                               starttime = post["datetime"],\
                                               )
        for j in range(1, segment+1):#更新环节
            segid = all_objects[j-1].id
            Segmnet_t.objects.filter(id = all_objects[j-1].id).update(sname = post["sname"+str(j)],\
                                                                    minute = post["minute"+str(j)],\
                                                                    content = post["introduce_c"+str(j)],\
                                                                    ratio = post["ratio"+str(j)],\
                                                                    )
            Table_t.objects.filter(tsegment_id = segid).delete()#先删除之前的所有表和权值，再添加新的权值
            mytable1 = Table_t(tsegment = all_objects[j-1],\
                               choice = 1,\
                               )
            mytable2 = Table_t(tsegment = all_objects[j-1],\
                               choice = 2,\
                               )
            mytable3 = Table_t(tsegment = all_objects[j-1],\
                               choice = 3,\
                               )
            mytable4 = Table_t(tsegment = all_objects[j-1],\
                               choice = 4,\
                               )
            mytable5 = Table_t(tsegment = all_objects[j-1],\
                               choice = 5,\
                               )

            if int(post["t2g"+str(j)]) > 0:#大于0为有效的表即教师选择的表，存储
                mytable1.save()
                Table_t.objects.filter(id = mytable1.id).update(ratio = int(post["t2g"+str(j)]))
            if int(post["t2s"+str(j)]) > 0:
                mytable2.save()
                Table_t.objects.filter(id = mytable2.id).update(ratio = int(post["t2s"+str(j)]))
            if int(post["g2g"+str(j)]) > 0:
                mytable3.save()
                Table_t.objects.filter(id = mytable3.id).update(ratio = int(post["g2g"+str(j)]))
            if int(post["gig"+str(j)]) > 0:
                mytable4.save()
                Table_t.objects.filter(id = mytable4.id).update(ratio = int(post["gig"+str(j)]))
            if int(post["self"+str(j)]) > 0:
                mytable5.save()
        return HttpResponseRedirect("/teacher/coursemanage/")
    dict3 = {"cid":cid, "pp":range(1, segment+1), 'seg_dict': seg_dict}
    return render_to_response("courseedit.html", dict3)

def editcourse_ajax(request):#接收HTML端发来的课程id，得到课程的所有信息通过ajax返回
    all_objects3 = []
    ret = []
    ret2 = []
    ret3 = []
    if request.POST:
        if request.is_ajax():
            cid = request.POST.get('name')
            all_objects = Course_t.objects.filter(id = cid)
            for courses in all_objects:
                ret.append(courses.cname)
                ret.append(courses.segmentsum)
                ret.append(courses.sum)
                ret.append(courses.groupsum)
                ret.append(courses.starttime)
                ret.append(courses.recommend)
                ret.append(courses.mytype)
            all_objects2 = Segmnet_t.objects.filter(tcourse_id = cid)
            for i in range(0, len(all_objects2)):
                temp = []
                temp.append(all_objects2[i].sname)
                temp.append(all_objects2[i].minute)
                temp.append(all_objects2[i].content)
                temp.append(all_objects2[i].ratio)
                ret2.append(temp)
                all_objects3 = Table_t.objects.filter(tsegment_id = all_objects2[i].id)
                temp2 = [0]*5
                for table in all_objects3:
                    temp2[table.choice - 1] = table.ratio
                ret3.append(temp2)
                
        dict2 = {"course":ret, "segment":ret2, "table":ret3, "segnum":ret[1]}
        print dict2
        return JsonResponse(dict2)

def addcourse(request):#教师添加课程
    thetype = 1
    all_objects2 = []
    all_objects3 = []
    clearsegment(request)
    clearcourse(request)
    all_objects = Course_t.objects.all()
    for i in range(len(all_objects)):
        if all_objects[i].isvalid == 1:
            all_objects2.append(all_objects[i])
            all_objects3.append(all_objects[i].id)
    if request.POST:
        post = request.POST
        check_box_list = request.POST.getlist("type")
        thetype = int(check_box_list[0])
        print type(request.user.id)
        newcourse = Course_t(\
                             teacher_id = request.user.id,\
                            cname = post["cname"].encode("utf-8"), \
                            sum = post["sum_s"],\
                            recommend = post["introduce_c"].encode("utf-8"),\
                            segmentsum = post["seg"],\
                            groupsum = post["group"],\
                            starttime = post["datetime"],\
                            mytype = thetype,\
                            )
        newcourse.save()
        return HttpResponseRedirect("/teacher/addcourse/addsegment/")
    dic = {'themodels':all_objects2, 'all_objects3':all_objects3}
    print all_objects3
    return render_to_response("addcourse.html", dic)

def ajax_course(request):#教师点击模板会显示模板信息，用于动态刷新网页
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            all_objects = Course_t.objects.filter(id = int(courseid))
            dataTojs = {'cname':all_objects[0].cname,\
                        'sum':all_objects[0].sum,\
                        'groupsum':all_objects[0].groupsum,\
                        'recommend':all_objects[0].recommend,\
                        'segmentsum':all_objects[0].segmentsum,\
                        'mytype':all_objects[0].mytype,\
                        'starttime':all_objects[0].starttime,\
                        }
            print all_objects[0].mytype
        return JsonResponse(dataTojs)
    
def addsegment(request):#教师添加环节
    segment = 0
    test = request.user.id
    themodels = []
    all_objects = Course_t.objects.filter(teacher_id = test)
    for i in range(len(all_objects)):   #从数据库中获得环节数
        if all_objects[i].isvalid == 0:
            segment = all_objects[i].segmentsum
            course_ins = all_objects[i]
    clearsegment(request)
    all_objects2 = Course_t.objects.filter(segmentsum = segment)#显示模板信息
    for i in range(len(all_objects2)): 
        if all_objects2[i].isvalid == 1:
            themodels.append(all_objects2[i])
    if request.POST:
        post = request.POST
        for i in range(1, segment+1):
            mysegment = Segmnet_t(tcourse = course_ins,\
                                  sname = post["sname"+str(i)],\
                                  minute = post["minute"+str(i)],\
                                  content = post["introduce_c"+str(i)],\
                                  ratio = post["ratio"+str(i)],\
                                  )
            mysegment.save()
        return HttpResponseRedirect("/teacher/addcourse/finally/")
    thedic = {'themodels': themodels, 'pp':range(1, segment+1)}
    return render_to_response("addsegment.html",thedic)

def ajax_segment(request):#同上动态刷新环节
    dataTojs = []
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            segment = Course_t.objects.filter(id  = int(courseid))
            dataTojs.append(segment[0].segmentsum) #把环节数传回JS
            all_objects = Segmnet_t.objects.filter(tcourse_id = int(courseid))
            for i in range(1, segment[0].segmentsum + 1):
                dataTojs.append(all_objects[i-1].sname)
                dataTojs.append(all_objects[i-1].minute)
                dataTojs.append(all_objects[i-1].content)
                dataTojs.append(all_objects[i-1].ratio) 
        thedic = {"pp":dataTojs}
        print dataTojs
        return JsonResponse(thedic)
    
def addfinally(request):#添加表格和表格权值
    mysegment = []
    seg_dict = {}
    mytable = []
    all_objects4 = []
    test = request.user.id
    themodels = []
    all_objects = Course_t.objects.filter(teacher_id = test)
    temp = []
    for i in range(len(all_objects)):   #从数据库中获得环节数
        if all_objects[i].isvalid == 0:
            courseid = all_objects[i]
    all_objects9 = Course_t.objects.filter(segmentsum = courseid.segmentsum)#显示模板信息
    for i in range(len(all_objects9)): 
        if all_objects9[i].isvalid == 1:
            themodels.append(all_objects9[i])
    all_objects2 = Segmnet_t.objects.filter(tcourse_id = courseid)
    for j in range(len(all_objects2)):
        if all_objects2[j].isvalid == 0:
            segmentid = all_objects2[j]
            temp.append(segmentid)
            mysegment.append(int(segmentid.id))
            seg_dict[j+1] = str(segmentid.ratio)
            all_objects3 = Table_t.objects.filter(tsegment_id = segmentid)
            mytable.append(all_objects3)
            all_objects4.append(Table_t.objects.filter(tsegment_id = segmentid))
    if request.POST:
        post = request.POST
        for i in range(0, len(temp)):
            mytable1 = Table_t(tsegment = temp[i],\
                               choice = 1,\
                               )
            mytable2 = Table_t(tsegment = temp[i],\
                               choice = 2,\
                               )
            mytable3 = Table_t(tsegment = temp[i],\
                               choice = 3,\
                               )
            mytable4 = Table_t(tsegment = temp[i],\
                               choice = 4,\
                               )
            mytable5 = Table_t(tsegment = temp[i],\
                               choice = 5,\
                               )
            j = i+1;
            if int(post["t2g"+str(j)]) > 0:
                mytable1.save()
                Table_t.objects.filter(id = mytable1.id).update(ratio = int(post["t2g"+str(j)]))
            if int(post["t2s"+str(j)]) > 0:
                mytable2.save()
                Table_t.objects.filter(id = mytable2.id).update(ratio = int(post["t2s"+str(j)]))
            if int(post["g2g"+str(j)]) > 0:
                mytable3.save()
                Table_t.objects.filter(id = mytable3.id).update(ratio = int(post["g2g"+str(j)]))
            if int(post["gig"+str(j)]) > 0:
                mytable4.save()
                Table_t.objects.filter(id = mytable4.id).update(ratio = int(post["gig"+str(j)]))
            if int(post["self"+str(j)]) > 0:
                mytable5.save()
                Table_t.objects.filter(id = mytable5.id).update(ratio = int(post["self"+str(j)]))
            Segmnet_t.objects.filter(id = temp[i].id).update(isvalid = 1)
            Course_t.objects.filter(id = courseid.id).update(isvalid = 1)
        return HttpResponseRedirect("/teacher/coursemanage/")
    print seg_dict
    dic = {'themodels': themodels,'seg_dict': seg_dict}
    return render_to_response("addfinally.html",dic)

def ajax_finally(request):#动态显示表格
    dataTojs = []
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            segment = Course_t.objects.filter(id  = int(courseid))
            dataTojs.append(segment[0].segmentsum) #把环节数传回JS
            all_objects = Segmnet_t.objects.filter(tcourse_id = int(courseid))
            for i in range(len(all_objects)):   #从数据库中获得环节数
                if all_objects[i].isvalid == 1:
                    sid = all_objects[i].id
                    all_objects2 = Table_t.objects.filter(tsegment_id = int(sid))
                    temp = [0]*5
                    for j in range(len(all_objects2)):
                        temp[all_objects2[j].choice - 1] = all_objects2[j].ratio
                    dataTojs.append(temp)
        thedic = {"pp":dataTojs}
        print thedic
        return JsonResponse(thedic)
    

def inclass(request):
    test = request.user.id
    all_objects = Course_t.objects.filter(teacher_id = test)
    tdic = {"mycourse":all_objects}
    return render_to_response("inclass.html", tdic)

def inclassajax(request):#处理下拉栏选择课程
    stu_name = []#存学生名
    stu_group = []#存学生分组
    stu_grade = []#存学生总成绩
    temp = []
    segment = []#存储当前选择课程的各个环节的名称、时间、介绍、比例
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            all_objects = Course_t.objects.filter(id = courseid)
            all_objects2 = Students.objects.filter(course_id = courseid)#获取本课程学生列表
            for stu in all_objects2:
                stuname = User.objects.filter(id = stu.stu_id)
                stu_name.append(stuname[0].username)
                stu_group.append(stu.group)
                stu_grade.append(stu.grade)
    #print stu_group
    theseg = Segmnet_t.objects.filter(tcourse_id = courseid)#记录当前选择课程的各个环节
    segment.append(all_objects[0].segmentsum)#第一个位置存储环节数量
    for seg in theseg:
        temp.append(seg.sname)
        temp.append(seg.minute)
        temp.append(seg.content)
        temp.append(seg.ratio)
        segment.append(temp)
        temp = []
    cdic = {"coursemess":all_objects[0].recommend, "groupnum":all_objects[0].sum / all_objects[0].groupsum,\
            "stuname":stu_name, "stugroup":stu_group, "stugrade":stu_grade,\
            "segment": segment}
    return JsonResponse(cdic)


def startcourse(request):#教师点击开始按钮
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            seg = request.POST.get('seg')
            print courseid
            if int(seg) == 1:#只有在第一环节点击开始按钮课程成绩才清零
                Students.objects.filter(course_id = courseid).update(
                                                            grade = 0,\
                                                              )
    return JsonResponse({"yy":1})

def nextsegment(request):#教师点击下一环节
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('name')
            seg = request.POST.get('seg')
            segment = Segmnet_t.objects.filter(tcourse_id = courseid)
            time = segment[int(seg)].minute
    cdic = {"time":time}
    return JsonResponse(cdic)

def Fenzu(request):#教师点击分组按钮随机分组
    fen_zu = 0
    stu = []#存储选择本课程的学生ID，用于产生随机分组
    stu_name = []#向教师提交分组后的学生列表
    stu_group = []
    stu_grade = []
    if request.POST:
        if request.is_ajax():
            fen_zu = request.POST.get('name')#fen_zu不为0时进行分组
            if not fen_zu == 0:
                all_objects = Course_t.objects.filter(id = fen_zu)
                all_objects2 = Students.objects.filter(course_id = fen_zu)
                for thestu in all_objects2:
                    stu.append(thestu.id)
                random.shuffle(stu) #将学生顺序打乱
                for i in range(1, all_objects[0].sum / all_objects[0].groupsum+1):
                    for j in range(0, all_objects[0].groupsum):
                        index = (i-1)*all_objects[0].groupsum + j
                        Students.objects.filter(id=stu[index]).update(group = i) 
                        all_objects3 = Students.objects.filter(id  = stu[index])
                        stuname = User.objects.filter(id = all_objects3[0].stu_id)
                        stu_name.append(stuname[0].username)
                        stu_group.append(all_objects3[0].group)
                        stu_grade.append(all_objects3[0].grade)
    cdic = {"stuname":stu_name, "stugroup":stu_group, "stugrade":stu_grade}      
    return JsonResponse(cdic)

def Randstu(request):#随机选择学生
    stu = []
    if request.POST:
        if request.is_ajax():
            fen_zu = request.POST.get('name')
            all_objects = Students.objects.filter(course_id = fen_zu)
            for mystudent in all_objects:
                stuname = User.objects.filter(id = mystudent.stu_id)
                stu.append(stuname[0].username)
    rstu = choice(stu)
    print rstu
    return JsonResponse({"cstu":rstu})

def Randgroup(request):#随机选择小组
    if request.POST:
        if request.is_ajax():
            fen_zu = request.POST.get('name')
            all_objects = Course_t.objects.filter(id = fen_zu)
    return JsonResponse({"czu":choice(range(1, all_objects[0].groupsum +1))})


def Grade_t(request):#教师发起全员评分请求
    course = []#存储选中课程信息
    segment = []#存储选中课程所有环节信息
    temp = []
    temp2 = []
    stuname = []#存储学生姓名
    stugroup = []#存储学生分组
    if request.POST:
        if request.is_ajax():
            print request.POST.get('name')
            all_course = Course_t.objects.filter(id = request.POST.get('name'))
            course.append(all_course[0].sum)
            course.append(all_course[0].groupsum)
            course.append(all_course[0].segmentsum)
            course.append(all_course[0].mytype)
            
            all_segment = Segmnet_t.objects.filter(tcourse_id = request.POST.get('name'))
            for thesegment in all_segment:
                temp.append(thesegment.sname)
                temp.append(thesegment.minute)
                temp.append(thesegment.ratio)
                
                all_table = Table_t.objects.filter(tsegment_id = thesegment.id)
                temp2 = []
                temp2 = [0]*5
                for thetable in all_table:
                    temp2[thetable.choice - 1] = thetable.ratio
                temp.append(temp2)
                segment.append(temp)
                temp = []
            
            all_student = Students.objects.filter(course_id = request.POST.get('name'))
            for thestu in all_student:
                haha = User.objects.filter(id = thestu.stu_id)
                stuname.append(haha[0].username)
                stugroup.append(thestu.group)
    #course [课程容量，小组人数，环节数，评分类型]
    #segment[[环节名称， 环节时间，环节比例， [评分1比例， 评分2比例， 评分3比例， 评分4比例， 评分5比例]], [...], [...], [...]]
    #stuname 存储选择该课程学生的姓名
    #stugroup 存储选择该课程的学生小组号

    cdic = {"course":course, "segment":segment, "stuname":stuname, "stugroup":stugroup}
    return JsonResponse(cdic)



def GfromT(request):#从前端获取教师对学生的评价信息，课程编号以及环节编号
    grade = []
    stuid = []#存储数据库中学生的学号
    state = 0#state为0时正常，当state为1时表示已到该课程最后一个环节
    if request.POST:
        if request.is_ajax():
            t_to_g = request.POST.getlist('grade1')#教师对小组整体评价
            t_to_s = request.POST.getlist('grade2')#教师对每位学生评价
            courseid = request.POST.get('courseid')#课程id
            segnum = request.POST.get('segnum')#环节编号，从0开始
            segment = Segmnet_t.objects.filter(tcourse_id = courseid)[int(segnum)]#segment就是当前环节
            table_g= Table_t.objects.filter(tsegment_id = segment.id, choice =1)
            stu = Students.objects.filter(course_id = courseid)
            for w in range(0, len(stu)):
                grade.append(stu[w].grade)#grade存储数据库中学生成绩，后面对其更新
                stuid.append(stu[w].id)
            if table_g:
                for i in range(1, int(t_to_g[0])+1):
                    t_to_g[i] = int(t_to_g[i]) * table_g[0].ratio / 100.00#按比例转化后的小组成绩
                for i in range(1, int(t_to_s[0])+1):#将教师对小组的评分更新
                    grade[i-1] = grade[i-1] + int(t_to_g[stu[i-1].group])     
            table_s= Table_t.objects.filter(tsegment_id = segment.id, choice =2)
            if table_s:
                for j in range(1, int(t_to_s[0])+1):
                    t_to_s[j] = int(t_to_s[j])* table_s[0].ratio / 100.00#按比例转化后的每位学生的成绩
                    grade[j-1] = grade[j-1] + int(t_to_s[j])#加上教师对每位同学的评分
            for k in range(0, int(t_to_s[0])):
                Students.objects.filter(id = stuid[k]).update(
                                                              grade = grade[k],\
                                                              )


            segment2 = Segmnet_t.objects.filter(tcourse_id = courseid)#这一部分是在点提交成绩按钮后判断是否为最后一个环节，若是则state为1
            time = segment2[int(segnum)].minute
            print int(segnum)
            print Course_t.objects.filter(id = courseid)[0].segmentsum
            if int(segnum) == Course_t.objects.filter(id = courseid)[0].segmentsum - 1:
                state = 1
                
                
            stu_name = []#存学生名
            stu_group = []#存学生分组
            stu_grade = []#存学生总成绩
            temp = []
            if request.POST:
                if request.is_ajax():
                    all_objects2 = Students.objects.filter(course_id = courseid)#获取本课程学生列表
                    for stu in all_objects2:
                        stuname = User.objects.filter(id = stu.stu_id)
                        stu_name.append(stuname[0].username)
                        stu_group.append(stu.group)
                        stu_grade.append(stu.grade)
            #print stu_group
            theseg = Segmnet_t.objects.filter(tcourse_id = courseid)#记录当前选择课程的各个环节
            for seg in theseg:
                temp.append(seg.sname)
                temp.append(seg.minute)
                temp.append(seg.content)
                temp.append(seg.ratio)
                temp = []
    cdic = {"stuname":stu_name, "stugroup":stu_group, "stugrade":stu_grade, "state":state}  
    return JsonResponse(cdic)