from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models

from db.commonmodel import Basemodels


# 轮播图
class Ad(Basemodels):
    name = models.CharField(max_length=100, verbose_name='轮播名称')
    sku = models.ForeignKey(to='SKU', verbose_name='sku_id')
    img = models.ImageField(upload_to='goods/%Y%m', default='goods/banner.png ', verbose_name='图片地址')
    order = models.IntegerField(verbose_name='排序')

    class Meta:
        db_table = 'ad'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 活动表
class Active(Basemodels):
    name = models.CharField(max_length=200, verbose_name='活动名称')
    img = models.ImageField(upload_to='goods/%Y%m', default='goods/s2.png ', verbose_name='图片地址')
    url = models.CharField(max_length=200, verbose_name='跳转的界面地址')
    sku = models.ForeignKey(to='SKU', verbose_name='sku_id')

    class Meta:
        db_table = 'active'
        verbose_name = '商品活动表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 活动专区
class Actarea(Basemodels):
    name = models.CharField(max_length=200, verbose_name='活动名称')
    comment = models.CharField(max_length=200, verbose_name='活动描述')
    order = models.IntegerField(verbose_name='排序')
    is_up = models.BooleanField(default=True, verbose_name='是否上架')

    class Meta:
        db_table = 'actarea'
        verbose_name = '活动专区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 活动专区商品
class Actgoods(Basemodels):
    actarea = models.ForeignKey(to='Actarea', verbose_name='活动专区id')
    sku = models.ForeignKey(to='SKU', verbose_name='商品id')

    class Meta:
        db_table = 'actgoods'
        verbose_name = '活动专区商品'
        verbose_name_plural = verbose_name


# 分类表
class Category(Basemodels):
    catename = models.CharField(max_length=30, verbose_name='分类名')
    comment = models.TextField(verbose_name='分类描述')

    class Meta:
        db_table = 'category'
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.catename


# 商品SKU表
class SKU(Basemodels):
    choices = (
        (1, '斤'),
        (2, '件'),
        (3, '箱'),
    )
    name = models.CharField(max_length=100, verbose_name='商品名')
    introduction = models.TextField(verbose_name='商品简介')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    unit = models.SmallIntegerField(choices=choices, verbose_name='单位')
    stock = models.IntegerField(verbose_name='库存')
    sell = models.IntegerField(verbose_name='销量')
    img = models.ImageField(upload_to='goods/%Y%m', default='goods/s2.png ', verbose_name='图片logo地址')

    def logo(self):
        return '<img src="{}{}" style="width:30px">'.format(settings.MEDIA_URL, self.img)

    logo.allow_tags = True
    logo.short_description = 'LOGO'

    is_up = models.BooleanField(default=True, verbose_name='是否上架')
    cate = models.ForeignKey(to='Category', verbose_name='分类id')
    spu = models.ForeignKey(to='SPU', verbose_name='spu_id')

    class Meta:
        db_table = 'SKU'
        verbose_name = '商品SKU表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品SPU表
class SPU(models.Model):
    name = models.CharField(max_length=200, verbose_name='spu名称')
    content = RichTextUploadingField(verbose_name='商品详情')

    class Meta:
        db_table = 'SPU'
        verbose_name = '商品SPU表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品相册
class GoodsImg(Basemodels):
    img = models.ImageField(upload_to='goods/%Y%m', default='goods/pic.png ', verbose_name='商品图片地址')
    sku = models.ForeignKey(to='SKU', verbose_name='sku_id')

    class Meta:
        db_table = ' goodsimg'
        verbose_name = '商品相册表'
        verbose_name_plural = verbose_name
