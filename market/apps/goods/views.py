from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect

from goods.models import Ad, Active, Actarea, Actgoods, Category, SKU


def index(request):
    # 轮播图
    banner = Ad.objects.filter()

    # 不规则活动
    act = Active.objects.all()

    # 特色专区
    actarea = Actarea.objects.all()

    context = {
        'banner': banner,
        'act': act,
        'actarea': actarea,
    }
    return render(request, 'goods/index.html', context)


def detail(request, id):
    sku = SKU.objects.get(id=id)
    context = {
        'sku': sku
    }
    return render(request, 'goods/detail.html', context)


def category(request, cate_id=0, order_id=0):
    # # 分类区
    # cate = Category.objects.filter()
    #
    # # 默认显示第一个
    # id = cate.first().id
    # # 商品列表
    # g_id = request.GET.get('id',default=id)
    #
    # # print(g_id)
    # cate1 = Category.objects.get(pk=g_id)
    # goodlist = cate1.sku_set.all().values()
    # data_dict_list = list(goodlist)
    #
    # context = {
    #     'cate': cate,
    #     'goodlist': goodlist,
    # }
    # if request.is_ajax():
    #     return JsonResponse({'list': data_dict_list})
    #
    # 获取到所有的分类
    category = Category.objects.filter()
    # 转换接收到分类id,如果不存在跳转到首页
    try:
        cate_id = int(cate_id)
        order_id = int(order_id)
    except:
        return redirect('goods:index')

    # 输入的值为0,返回第一个分类数据,分类id为第一个分类数据的id,否则等于收到的id值
    if cate_id == 0:
        cate = category.first()
        cate_id = cate.id
    else:
        cate = Category.objects.get(pk=cate_id)
    # 获取分类下的商品

    # 根据选择的排序id来排序
    order_rule = ['id', '-sell', '-price', 'price', '-add_time']
    try:
        order = order_rule[order_id]
    except:
        order = order_rule[0]
    goodlist = cate.sku_set.all()
    goodlist = goodlist.order_by(order)

    # 分页
    paginator = Paginator(goodlist, 1)
    page = request.GET.get('p', 1)
    try:
        goodlist = paginator.page(page)
    except PageNotAnInteger:
        goodlist = paginator.page(1)
    except EmptyPage:
        goodlist = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'cate_id': cate_id,
        'goodlist': goodlist,
        'order_id': order_id,
    }
    return render(request, 'goods/category.html', context)
