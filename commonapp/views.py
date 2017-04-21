# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from commonapp.models import User_class
from django.contrib import auth

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