# coding:utf-8
from django.shortcuts import render,redirect
from django.db import transaction
from models import *
from df_cart.models import CartInfo
from users.deractor import login
from datetime import datetime
# Create your views here.


@transaction.atomic
def order(request):
    # 获取用户信息
    post = request.POST
    address = post.get('address')
    cart_ids = post.getlist('cart_id')
    sid = transaction.savepoint()
    try:
        # 创建主订单对象
        order = OrderInfo()
        order_time = datetime.now()
        uid = request.session['user_id']
        # 拼接订单号：日期和用户名拼接
        order.oid = '%s%d'%(order_time.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = order_time
        order.oaddress = address
        order.ototal = 0
        order.save()
        # 计算总金额
        total=0
        # 库存判断,下订单的时候是否可以购买
        for cart_id in cart_ids:
            cart = CartInfo.objects.get(pk=cart_id)
            if cart.goods.gkucun >= cart.count:
                # 库存大于购物车数量，可以购买
                # 购买后库存量变化，减少库存量，并写入数据库
                cart.goods.gkucun -= cart.count
                cart.save()
                # 创建详单对象，将购买记录写入详单表
                orderdetail = OrderDetailInfo()
                orderdetail.order = order
                orderdetail.price = cart.goods.gprice
                orderdetail.count = cart.count
                orderdetail.goods = cart.goods
                orderdetail.save()
                #  计算总金额
                total += cart.goods.gprice*cart.count
                # 删除购物车里面已购买的商品
                cart.delete()
            else:
                # 库存量不足，不允许下单
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')

        #   总价写入数据库
        order.ototal = total
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/users/order/')
    except:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')

@login
def pay(request,id):
    order=OrderInfo.objects.get(oid=id)
    order.oIsPay=True
    order.save()
    return redirect('/users/order/')