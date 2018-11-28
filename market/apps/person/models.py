from django.core.validators import RegexValidator
from django.db import models

# 登录注册表
from db.commonmodel import Basemodels


class register(models.Model):
    tel = models.CharField(max_length=11)
    password = models.CharField(max_length=20)
    check = models.CharField(max_length=10, default=0)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'register'

    def __str__(self):
        return self.tel


# 个人信息表
class User_info(models.Model):
    choice = [(1, '男'),
              (2, '女')]
    log_id = models.OneToOneField(to='register')
    head_sculpture = models.CharField(max_length=100, default=0)
    head_img = models.ImageField(upload_to='', default='images/infortx.png', verbose_name='头像')
    nickname = models.CharField(max_length=30)
    sex = models.SmallIntegerField(choices=choice)
    birthday = models.DateField()
    school = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    hometown = models.CharField(max_length=200)
    tel = models.CharField(max_length=11)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    isdelete = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return self.nickname


# 收货地址表
class Address(Basemodels):
    log = models.ForeignKey(to='register', verbose_name='用户标识')
    name = models.CharField(max_length=30, verbose_name='用户姓名')
    tel = models.CharField(max_length=11, verbose_name='用户号码',
                           validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误')])
    hcity = models.CharField(max_length=100, verbose_name="省")
    hproper = models.CharField(max_length=100, blank=True, default='', verbose_name="市")
    harea = models.CharField(max_length=100, blank=True, default='', verbose_name="区")
    brief = models.CharField(max_length=255, verbose_name="详细地址")
    isDefault = models.BooleanField(default=False, blank=True, verbose_name="是否设置为默认")

    class Meta:
        db_table = 'address'
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
