# coding:utf-8
from django.shortcuts import render,redirect
from models import userInfo
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from hashlib import sha1
# Create your views here.


def login(fun):
    def login_fun(request, *args, **kwargs):

         if request.session. has_key('user_id'):
             return fun(request, *args, **kwargs)

         else:
             if request.is_ajax():
                 return JsonResponse({'islogin':0})
             else:
                 return HttpResponseRedirect('/users/login/')
             # red.set_cookie('url', request.get_full_path())
             # return red
    return login_fun