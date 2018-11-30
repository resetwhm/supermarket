import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from goods.models import SKU
from order.forms import AddressForm, AddresseditForm
from order.models import Transport, Order_info, Order_goods
from person.models import Address

from datetime import datetime


# 地址三级联动
def address(request):
    if request.method == "POST":
        data = request.POST
        hcity = data.get('hcity')
        hproper = data.get('hproper')
        harea = data.get('harea')
        context = {
            'hcity': hcity,
            'hproper': hproper,
            'harea': harea,
        }
        return render(request, 'order/address.html', context)
    else:
        return render(request, 'order/address.html')


def addedit(request):
    if request.method == "POST":
        data = request.POST
        id = data.get('id')
        # print(id)
        address = Address.objects.get(pk=id)
        hcity = data.get('hcity')
        hproper = data.get('hproper')
        harea = data.get('harea')
        context = {
            'id': id,
            'hcity': hcity,
            'hproper': hproper,
            'harea': harea,
            'address': address
        }
        return render(request, 'order/address_edit.html', context)
    else:
        return render(request, 'order/address_edit.html')


# 添加地址
def add(request):
    if request.method == "POST":
        id = request.session.get('id')
        data = request.POST.dict()
        data['id'] = id
        form = AddressForm(data)
        # print(data.isDefault)
        if form.is_valid():
            data = form.cleaned_data
            data["log_id"] = id
            Address.objects.create(**data)
            return redirect('person:gladdress')
        else:
            context = {
                'error': form.errors,
                'form': form
            }
            return render(request, 'order/address.html', context)
    else:
        return render(request, 'order/address.html')


# 修改地址
def edit(request, id):
    if request.method == "GET":
        log_id = request.session.get('id')
        try:
            address = Address.objects.get(pk=id, log_id=log_id)
        except Address.DoesNotExist:
            return redirect('person:gladdress')
        # print(address.isDefault)
        context = {
            "address": address,
            'id': address.id
        }
        return render(request, 'order/address_edit.html', context)
    else:
        log_id = request.session.get('id')
        data = request.POST.dict()
        data['id'] = id
        form = AddresseditForm(data)
        # print(data)
        if form.is_valid():
            data = form.cleaned_data
            Address.objects.filter(log_id=log_id).update(isDefault=False)
            Address.objects.filter(pk=id, log_id=log_id).update(**data)
            return redirect('person:gladdress')
        else:
            context = {
                'error': form.errors,
                'form': form
            }
            return render(request, 'order/address.html', context)


def delete(request):
    log_id = request.session.get('id')
    if request.method == "POST":
        id = request.POST.get("id")
        Address.objects.filter(pk=id, log_id=log_id).update(isdelete=True)
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 1, "err": "请求方式错误"})


def default(request):
    log_id = request.session.get('id')
    if request.method == "POST":
        id = request.POST.get("id")
        Address.objects.filter(log_id=log_id).update(isDefault=False)
        Address.objects.filter(pk=id, log_id=log_id).update(isDefault=True)
        return JsonResponse({"code": 0})
    else:
        return JsonResponse({"code": 1, "err": "请求方式错误"})


# 添加订单
def addorder(request):
    id = request.session.get('id')
    goods = request.POST.get('goods')
    r = get_redis_connection('default')
    goods = goods.strip(" ")
    goods = goods.split(" ")
    order_key = "order_key_{}".format(id)
    user_key = "user_key_{}".format(id)
    r.delete(order_key)
    for sku_id in goods:
        num = r.hget(user_key, sku_id)
        num = int(num)
        r.hset(order_key, sku_id, num)
    return JsonResponse({"code": 0})


# 购物车
def tureorder(request):
    if request.method == 'POST':
        # 是否登录
        id = request.session.get("id")
        if id is None:
            return JsonResponse({"code": 1, "err": "用户没有登录"})

        address = request.POST.get('address')
        sku_id = request.POST.getlist("sku_id")
        transport = request.POST.get("transport")
        comment = request.POST.get('comment')

        # 参数是否都存在
        if not (address and sku_id and transport):
            return JsonResponse({"code": 2, "err": "参数错误"})

        # 参数是否符合要求
        try:
            address = int(address)
            transport = int(transport)
            sku = [int(sku) for sku in sku_id]
        except:
            return JsonResponse({"code": 3, "err": "参数错误"})

        # 所传信息是否存在
        try:
            address = Address.objects.get(pk=address)
        except address.DoesNotExist:
            return JsonResponse({"code": 4, "err": "地址不存在"})

        try:
            transport = Transport.objects.get(pk=transport)
        except transport.DoesNotExist:
            return JsonResponse({"code": 5, "err": "运输方式不存在"})

        # 保存订单信息
        r = get_redis_connection('default')
        user_key = "user_key_{}".format(id)
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        ordernum = "{}{}{}".format(time, id, random.randint(1000, 99999))
        address_brief = "{}{}{}{}".format(address.hcity, address.hproper, address.harea, address.brief)
        # 存储订单信息表
        order = Order_info.objects.create(
            ordernum=ordernum,
            user_id=id,
            name=address.name,
            tel=address.tel,
            address=address_brief,
            transport=transport.name,
            trans_money=transport.money,
        )
        order_money = 0
        total = 0
        for sku_id in sku:
            try:
                goodssku = SKU.objects.get(pk=sku_id, isdelete=False, is_up=True)
            except SKU.DoesNotExist:
                return JsonResponse({"code": 6, "err": "商品不存在"})

            # 获取商品的数量
            count = r.hget(user_key, sku_id)
            count = int(count)
            # 保存订单商品信息
            Order_goods.objects.create(
                order=order,
                sku=goodssku,
                number=count,
                price=goodssku.price
            )
            # 检查库存是否充足
            if goodssku.stock < count:
                return JsonResponse({"code": 7, "err": "库存不足"})
            # 销量增加,库存减少
            goodssku.sell += count
            goodssku.stock -= count

            # 计算商品价格
            order_money += goodssku.price * count

        # 计算总金额
        total += order_money + transport.money

        # 保存价格和备注信息
        try:
            order.order_money = order_money
            order.total = total
            order.comment = comment
            order.save()
        except:
            return JsonResponse({"code": 8, "err": "总价保存失败"})
        # 删除购物车的商品信息
        r.hdel(user_key, *sku)
        return JsonResponse({"code": 0, "ordernum": ordernum})

    else:
        id = request.session.get('id')
        r = get_redis_connection('default')
        goodslist = []
        order_key = "order_key_{}".format(id)
        goods = r.hgetall(order_key)
        price = 0
        for sku_id in goods:
            sku = SKU.objects.get(pk=sku_id)
            r = get_redis_connection('default')
            num = r.hget(order_key, sku_id)
            sku.num = int(num)
            # 计算总价
            price += sku.price * sku.num
            goodslist.append(sku)
        transport = Transport.objects.all().order_by('money')
        address = Address.objects.filter(log_id=id, isdelete=False).order_by("isDefault").first()
        context = {
            "address": address,
            "goodslist": goodslist,
            "transport": transport,
        }
        return render(request, 'cart/tureorder.html', context)


def order(request):
    ordernum = request.GET.get("ordernum")
    order = Order_info.objects.get(ordernum=ordernum)
    context = {
        "order": order
    }
    return render(request, 'cart/order.html', context)
