# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from commonapp.models import User_class, Talk
from django.contrib import auth
from django.http import JsonResponse

def menu(request):#开始菜单
    return render_to_response("start.html")

def logcheck(request):
    test = request.user.id
    user_t = User.objects.filter(id = test)
    user_c = User_class.objects.filter(person__exact = user_t)
    return user_c.values()[0]['clas']
 
def logout(request):#学生教师注销登陆
    auth.logout(request)
    return render_to_response("start.html")

def forgot(request):#学生教师忘记密码
    errors = []
    if request.POST:
        post = request.POST
        for i in post.keys():
            if post[i] == "":
                errors.append("Please input " + i)
        if post["pass"] != post["re_pass"]:
            errors.append("Password doesn\'t match")
        if not User.objects.filter(username = post["user"]).values()[0]['email'] == post["email"]:
            errors.append("Email doesn\'t match")
        if errors == []:
            if not (User.objects.filter(username = post["user"])):
                return render_to_response("prj_forgot_password.html", {'errors': ["User not exist!"]})
            u = User.objects.get(username__exact = post["user"])
            u.set_password(post["pass"])
            u.save()
            return render_to_response("start.html")
    return render_to_response("prj_forgot_password.html", {'errors': errors, })

def Talkajax(request):#教师/学生选择好课程后, 在前端显示留言信息
    message_id = []
    message_message = []
    message_name = []
    message_time = []
    if request.POST:
        if request.is_ajax():
            courseid = request.POST.get('courseid')#课程id
            all_message = Talk.objects.filter(courseid_id = courseid)
            for mes in all_message:
                message_id.append(mes.id)
                message_message.append(mes.message)
                message_name.append(mes.name)
                message_time.append(mes.time)
            num = len(message_id)
    cdic = {"id":message_id, "message":message_message, "name":message_name, "time":message_time, "num":num}
    return JsonResponse(cdic)