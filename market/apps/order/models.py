# from django.db import models
#
# from db.commonmodel import Basemodels
#
#
# class Paymethod(Basemodels):
#     pay_name = models.CharField(verbose_name='支付方式', max_length=20)
#
#     class Meta:
#         db_table = 'paymethod'
#         verbose_name = "支付方式"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.pay_name
#
#
# class Transport(Basemodels):
#     name = models.CharField(verbose_name='配送方式', max_length=20)
#     money = models.DecimalField(verbose_name='金额', max_digits=9, decimal_places=2, default=0)
#
#     class Meta:
#         db_table = 'transport'
#         verbose_name = "配送方式"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
