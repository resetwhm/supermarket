from django.db import models

from db.commonmodel import Basemodels


class Paymethod(Basemodels):
    pay_name = models.CharField(verbose_name='支付方式', max_length=20)
    logo = models.ImageField(upload_to='pay/', verbose_name='logo')

    class Meta:
        db_table = 'paymethod'
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Transport(Basemodels):
    name = models.CharField(verbose_name='配送方式', max_length=20)
    money = models.DecimalField(verbose_name='金额', max_digits=9, decimal_places=2, default=0)

    class Meta:
        db_table = 'transport'
        verbose_name = "配送方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Order_info(Basemodels):
    choices = [
        (0, '待付款'),
        (1, '退发货'),
        (2, '待收货'),
        (3, '待评价'),
        (4, '已完成'),
    ]
    ordernum = models.CharField(max_length=255, verbose_name='订单编号', default=0)
    user = models.ForeignKey(to="person.register", verbose_name='用户id')
    name = models.CharField(max_length=30, verbose_name='收货人姓名')
    tel = models.CharField(max_length=11, verbose_name='收货人电话')
    address = models.CharField(max_length=200, verbose_name='地址信息')
    order_status = models.SmallIntegerField(choices=choices, default=0, verbose_name='订单状态')
    transport = models.CharField(max_length=30, verbose_name='运输方式')
    trans_money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='运输金额')
    paymethod = models.ForeignKey(to='Paymethod', verbose_name='支付方式id', null=True, blank=True)
    order_money = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='订单商品金额', default=0)
    total = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='订单总金额', default=0)
    real_money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='实付金额')
    comment = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'order_info'
        verbose_name = '订单信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ordernum


class Order_goods(Basemodels):
    order = models.ForeignKey(to='Order_info', verbose_name='订单id')
    sku = models.ForeignKey(to='goods.SKU', verbose_name='商品sku_id')
    number = models.IntegerField(verbose_name='商品数量')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='商品价格')

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku
