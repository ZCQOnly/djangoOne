# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest,JsonResponse
from users.deractor import *
from models import *
from users.models import userInfo
# Create your views here.


@login
def cart(request):
    cid = request.session['user_id']
    cartlist = CartInfo.objects.filter(user_id=cid)
    context = {'title': '购物车','cartlist': cartlist, 'page_name':1,
    }
    return render(request, 'df_cart/cart.html', context)

@login
def add(request, id, count):
    carts = CartInfo.objects.filter(goods_id=id).filter(user_id=request.session['user_id'])
    if len(carts)==0:
        cart = CartInfo()
        cart.goods_id = int(id)
        cart.user_id = request.session['user_id']
        cart.count = int(count)
        cart.save()
    else:
        cart = carts[0]
        if cart.count<cart.goods.gkucun:
            cart.count += int(count)
        cart.save()
    if request.is_ajax():
        return JsonResponse({'count': CartInfo.objects.filter(user_id=request.session['user_id']).count()})
    else:
        return redirect('/cart/')

@login
def amount(request,id,count):
    try:
        cart = CartInfo.objects.get(id=int(id))
        countone = 1
        countone = cart.count
        cart.count = int(count)
        cart.save()
        # 用来判断修改是否成功
        num={'num': 0}
    except Exception as e:
        num = {'num': countone}
    return JsonResponse(num)


@login
def delete(request,id):
    try:
        cart = CartInfo.objects.get(id=int(id))
        # 物理删除
        cart.delete()
        # 用来判断删除是否成功
        num = {'num': 1}
    except Exception as e:
        num={'num': 0}
    return JsonResponse(num)

@login
def order(request):
    # 获取当前用户ｉｄ，表示用户登陆
    user=userInfo.objects.get(id=request.session['user_id'])
    # 通过复选框ｎａｍｅ键来获得有哪些在购物车内
    cart_ids = request.GET.getlist('cart_id')
    # cart_ids1=[int(item) for item in cart_ids]
    # 判断购物车里的商品有哪些商品被选中
    carts = CartInfo.objects.filter(id__in=cart_ids)
    context = {'title':'提交订单','user':user,'cart_list':carts,'page_name':1}
    return render(request,'df_cart/order.html',context)