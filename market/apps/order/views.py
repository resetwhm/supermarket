from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection

from order.forms import AddressForm, AddresseditForm
from person.models import Address


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


# 购物车
def tureorder(request):
    id = request.session.get('id')
    address = Address.objects.filter(log_id=id, isDefault=True, isdelete=False).first()
    context = {
        "address": address
    }
    return render(request, 'cart/tureorder.html', context)


def order(request):
    return render(request, 'cart/order.html')
