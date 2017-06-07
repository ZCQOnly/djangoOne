# coding:utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    typelist = TypeInfo.objects.all()
    list = []
    for type in typelist:
        list.append({
            'type':type,
            'hot_click': type.goodsinfo_set.order_by('-gclick')[0:3],
            'hot_new': type.goodsinfo_set.order_by('-id')[0:4]
        })
    context = {'title': '首页', 'list': list}
    return render(request, 'df_goods/index.html', context)


def list(request, tid, pindex, sort):
    # 获取当前商品分类类型，是一个属性，即当前是什么类型
    gtype = TypeInfo.objects.get(id=int(tid))
    # 获取当前商品类型前两个新品的信息列表
    newslist = gtype.goodsinfo_set.order_by('-id')[0:2]
    # 获取当前分类的所有商品的信息列表
    goodslist = GoodsInfo.objects.filter(gtype_id=int(tid))
    if sort == '1':
        goodslist = goodslist.order_by('-id')
        active = ['active', '', '']
    elif sort == '2':
        goodslist = goodslist.order_by('-gprice')
        active = ['', 'active', '']
    elif sort == '3':
        goodslist = goodslist.order_by('-gclick')
        active = ['', '', 'active']
    # 创建paginator对象，同时调用了其init（）方法，一页显示多少商品
    paginator = Paginator(goodslist, 5)
    # 获取当前页的所有数据
    page = paginator.page(int(pindex))
    context = {'title': '商品列表', 'gtype': gtype,
               'tid': tid, 'page': page, 'sort': sort,
               'newslist': newslist, 'active': active,
                'pindex': pindex,}
    return render(request, 'df_goods/list.html', context)


def detail(request, id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick = goods.gclick+1
    goods.save()
    goods_new = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': goods.gtype.ttitle,
               'newslist': goods_new,
               'id': id,
               'goods': goods,
               }
    response = render(request, 'df_goods/detail.html', context)

    # 用户中心信息维护
    browse = request.COOKIES.get('browse', '')
    # 判断是否有浏览记录,如果有浏览记录，首先判断是否有重复的，然后判断总数
    # 超过６的话就删除最后一个
    if browse != '':
        # 如果有浏览记录，将这个记录拆分成列表来进行增删改查
        browse_list = browse.split(',')
        if browse_list.count(id) >= 1:
            browse_list.remove(id)
        browse_list.insert(0, id)
        if len(browse_list) >= 6:
            browse_list.pop()
        browse2 = ','.join(browse_list)
        response.set_cookie('browse',browse2)
    else:
        response.set_cookie('browse', id)
    return response


from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title']=self.request.GET.get('q')
        return extra

# 由于首页＼列表页都需要显示购物车里面商品的数量，所以建立函数来实现数量的显示
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(request.session['user_id']).count()
    else:
        return 0