from django.http import JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from goods.models import SKU


def shopcart(request):
    user_id = request.session.get('id')
    if user_id is None:
        return redirect('person:login')
    r = get_redis_connection('default')
    user_key = "user_key_{}".format(user_id)
    cartgoods = r.hgetall(user_key)

    cartlist = []

    sku = request.POST.get("sku_id")
    if sku:
        sku = int(sku)
        # num = r.hget(user_key, sku)
        # num = num.decode('utf-8')
        r.hdel(user_key, sku)
        return JsonResponse({"code": 0})

    for k, v in cartgoods.items():
        sku_id = k.decode('utf-8')
        goods = SKU.objects.get(pk=sku_id)
        goods.num = v.decode('utf-8')
        cartlist.append(goods)

    context = {
        'goods': cartlist,

    }
    return render(request, 'cart/shopcart.html', context)


def addcart(request):
    # 判断用户是否登录
    user_id = request.session.get('id')
    if user_id is None:
        return JsonResponse({"code": 1, "err": "没有登录"})

    # 获取参数
    sku_id = request.POST.get('sku_id')
    num = request.POST.get('num')

    try:
        sku_id = int(sku_id)
        num = int(num)
    except:
        return JsonResponse({"code": 2, "err": "参数错误"})

    # 判断商品是否存在
    try:
        goods = SKU.objects.get(pk=sku_id)
    except:
        return JsonResponse({"code": 4, "err": "商品不存在"})

    # 判断库存
    if goods.stock < num:
        return JsonResponse({"code": 3, "err": "参数错误"})

    # 将数据存入redis中
    r = get_redis_connection('default')
    user_key = "user_key_{}".format(user_id)
    mycart = r.hincrby(user_key, sku_id, num)
    total = 0
    totalcart = r.hvals(user_key)
    for v in totalcart:
        total += int(v)
    if mycart == 0:
        r.hdel(user_key, sku_id)
    return JsonResponse({"code": 0, "total": total})


