# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest,JsonResponse
from users.deractor import *
from models import *
# Create your views here.


@login
def cart(request):
    cid = request.session['user_id']
    cartlist = CartInfo.objects.filter(user_id=cid)
    context = {'title': '购物车','carts': cartlist, 'page_name':1,
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