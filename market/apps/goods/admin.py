from django.contrib import admin

# Register your models here.
from goods.models import Ad, Active, Actarea, Actgoods, Category, SKU, SPU, GoodsImg


class SKUAdminInline(admin.StackedInline):
    model = GoodsImg
    extra = 2

class AreagoodsInline(admin.StackedInline):
    model = Actgoods
    extra = 2

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['name', 'sku', 'img', 'order']


@admin.register(Active)
class ActiveAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['name', 'img', 'url', 'sku']


@admin.register(Actarea)
class ActareaAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['name', 'comment', 'order', 'is_up']
    inlines = [AreagoodsInline]


@admin.register(Actgoods)
class ActgoodsAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['actarea', 'sku']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['catename', 'comment']


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['name', 'introduction', 'price', 'unit', 'stock', 'sell', 'logo', 'is_up', 'cate', 'spu']
    inlines = [SKUAdminInline]


@admin.register(SPU)
class SPUAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['name', 'content']


@admin.register(GoodsImg)
class GoodsImgAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['img', 'sku']
