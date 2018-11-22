from django.db import models


# 登录注册表
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
    head_img = models.ImageField(upload_to='head', default='images/infortx.png', verbose_name='头像')
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
class Address(models.Model):
    log = models.ForeignKey(to='register')
    name = models.CharField(max_length=30)
    tel = models.CharField(max_length=11)
    Sheng_id = models.SmallIntegerField(default=0)
    Shi_id = models.SmallIntegerField(default=0)
    Qu_id = models.SmallIntegerField(default=0)
    Stree_id = models.SmallIntegerField(default=0)
    address_comment = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    isdelete = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return self.address_comment
