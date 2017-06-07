# coding:utf-8
from django.shortcuts import render,redirect
from models import userInfo
from df_goods.models import GoodsInfo
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from hashlib import sha1
import deractor
# Create your views here.


def register(request):
    title = '天天生鲜－注册'
    context = {'title': title}
    return render(request, 'users/register.html', context)


def register_handle(request):
    dict = request.POST
    username = dict.get('user_name')
    passwd = dict.get('pwd')
    # print passwd
    passwd2 = dict.get('cpwd')
    umail = dict.get('email')
    if passwd != passwd2:
        return redirect('/users/register/')
    s1 = sha1()
    s1.update(passwd)
    passwd3 = s1.hexdigest()
    user = userInfo()
    user.passwd = passwd3
    user.username = username
    user.umail = umail
    user.save()
    return redirect('/users/login/')


def register_exist(request):
    username = request.GET.get('username')
    count = userInfo.objects.filter(username=username).count()
    context = {'count': count}
    return JsonResponse(context)


def login(request):
    title = '天天生鲜-登陆'
    username = request.COOKIES.get('username', '')
    context = {'title': title, 'error_name': 0, 'error_pwd': 0, 'username': username}
    return render(request, 'users/login.html', context)


def login_handle(request):
    post = request.POST
    username = post.get('username')
    passwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = userInfo.objects.filter(username=username)
    # print username
    if len(users) == 1:
        s1 = sha1()
        s1.update(passwd)
        print s1.hexdigest()
        print users[0].passwd
        if s1.hexdigest() == users[0].passwd:
            url = request.COOKIES.get('red_url', '/')
            # print url
            # red = HttpResponseRedirect(url)
            red = redirect(url)
            red.set_cookie('url', '', max_age=-1)
            print
            if jizhu != 0:
                red.set_cookie('username', username)
            else:
                red.set_cookie('username', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = username
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'username': username, 'upwd':passwd}
            return render(request,'users/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'username': username, 'upwd': passwd}
        return render(request,'users/login.html',context)


def logout(request):
    request.session.flush()
    return redirect('/')


@deractor.login
def info(request):
    umail = userInfo.objects.get(id=request.session['user_id']).umail
    uaddress = userInfo.objects.get(id=request.session['user_id']).uaddress
    utel = userInfo.objects.get(id=request.session['user_id']).utel

    goods_list = []
    goods_ids = request.COOKIES.get('browse', '')
    if goods_ids != '':
        id_list = goods_ids.split(',')
        for ids in id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(ids)))
    context={'title': '用户中心',
             'username': request.session['user_name'],
             'umail': umail,
             'uaddress': uaddress,
             'utel': utel,
             'page_name':1,
             'active': ['active', '', ''],
             'goods_list':goods_list,
             }
    return render(request, 'users/user_center_info.html', context)


@deractor.login
def order(request):
    context = {'title': '用户中心', 'active': ['', 'active', ''], 'page_name':1}
    return render(request, 'users/user_center_order.html', context)


@deractor.login
def site(request):
    user = userInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.uddress = post.get('uaddress')
        user.upost = post.get('upost')
        user.utel = post.get('utel')
        user.ushou = post.get('ushou')
        user.save()
    context = {'title': '用户中心','user': user, 'active': ['', '', 'active'], 'page_name':1}
    return render(request, 'users/user_center_site.html', context)






