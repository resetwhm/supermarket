import os
from urllib.parse import urlparse, parse_qs

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from goods.models import SKU
from market.settings import BASE_DIR
from order.models import Order_info
# from utils.alipay.alipay import AliPay
from alipay import AliPay
import time


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


def pay(request):
    # """支付宝支付成功后通知接口验证"""
    # order_id = request.GET.get("out_trade_no")
    # order = Order_info.objects.get(ordernum=order_id)
    # price = str(order.total)
    # # print(order.ordernum)
    # # 传递参数初始化支付类
    # alipay = AliPay(
    #     appid="2016092400584100",  # 设置签约的appid
    #     app_notify_url="http://127.0.0.1:8000/cart/pay/",  # 异步支付通知url
    #     app_private_key_path=os.path.join(BASE_DIR, 'apps/utils/alipay/ying_yong_si_yao.txt'),  # 设置应用私钥
    #     alipay_public_key_path=os.path.join(BASE_DIR, 'apps/utils/alipay/zhi_fu_bao_gong_yao.txt'),
    #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    #     debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
    #     return_url="http://127.0.0.1:8000/cart/pay/"  # 同步支付通知url
    # )
    # # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
    #
    # url = alipay.direct_pay(
    #     subject="测试订单",  # 订单名称
    #     # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
    #     out_trade_no=order.ordernum,  # 订单号
    #     total_amount=price,  # 支付金额
    #     return_url="http://127.0.0.1:8000/cart/pay/"  # 支付成功后，跳转url
    # )
    # # 接收支付宝支付成功后，向我们设置的同步支付通知url，请求的参数
    # return_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    #
    # # 将同步支付通知url,传到urlparse
    # o = urlparse(return_url)
    # # 获取到URL的各种参数
    # query = parse_qs(o.query)
    # # 定义一个字典来存放，循环获取到的URL参数
    # processed_query = {}
    # # 将URL参数里的sign字段拿出来
    # ali_sign = query.pop("sign")[0]
    #
    # # 循环出URL里的参数
    # for key, value in query.items():
    #     # 将循环到的参数，以键值对形式追加到processed_query字典
    #     processed_query[key] = value[0]
    # # 将循环组合的参数字典，以及拿出来的sign字段，传进支付类里的verify方法，返回验证合法性，返回布尔值，True为合法，表示支付确实成功了，这就是验证是否是伪造支付成功请求
    # res = alipay.verify(processed_query, ali_sign)
    # print(alipay.verify(processed_query, ali_sign))
    # if res is False:
    #     context = {
    #         "mess": "支付失败"
    #     }
    # else:
    #     context = {
    #         "mess": "支付成功"
    #     }
    #     Order_info.objects.filter(ordernum=order_id).update(order_status=1)
    # # 如果别人伪造支付成功请求，它不知道我们的支付宝公钥，伪造的就无法通过验证，测试可以将支付宝公钥更改一下，在验证就会失败，别忘了改回来
    # return render(request, 'cart/pay.html', context)

    # try:
    #     order = Order_info.objects.get(ordernum=out_trade_no)
    # except Order_info.DoesNotExist:
    #     return redirect('cart:shopcart')

    # print(out_trade_no)

    app_private_key_string = open(os.path.join(BASE_DIR, 'apps/utils/alipay/ying_yong_si_yao.txt')).read()
    alipay_public_key_string = open(os.path.join(BASE_DIR, 'apps/utils/alipay/ying_yong_gong_yao.txt')).read()

    alipay = AliPay(
        appid="2016092400584100",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    out_trade_no = request.GET.get("out_trade_no")
    paid = False
    for i in range(3):
        result = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            break
        else:
            time.sleep(3)

    if paid is False:
        context = {
            "mess": "支付失败"
        }
    else:
        context = {
            "mess": "支付成功"
        }
        Order_info.objects.filter(ordernum=out_trade_no, order_status=0).update(order_status=1)
    return render(request, 'cart/pay.html', context)
