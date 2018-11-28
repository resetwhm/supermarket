from django.http import HttpResponse
from django.shortcuts import render, redirect

from order.forms import AddressForm
from person.models import Address


def tureorder(request):
    good_id = request.GET.get('good_id')
    context = {
        'good_id': good_id
    }
    return render(request, 'order/tureorder.html', context)


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


# 添加地址
def add(request):
    if request.method == "POST":
        id = request.session.get('id')
        data = request.POST
        form = AddressForm(data)
        print(data)
        isDefault = data.get('isdefault')
        if form.is_valid():
            data = form.cleaned_data
            hcity = data.get('hcity')
            hproper = data.get('hproper')
            harea = data.get('harea')
            brief = data.get('brief')
            name = data.get('name')
            tel = data.get('tel')

            print(hcity, hproper, harea, brief, name, tel)
            if isDefault:
                Address.objects.create(log_id=id, hcity=hcity, hproper=hproper, harea=harea, brief=brief, name=name,
                                   tel=tel, isDefault=isDefault)
            else:
                Address.objects.create(log_id=id, hcity=hcity, hproper=hproper, harea=harea, brief=brief, name=name,
                                       tel=tel)
            return redirect('person:gladdress')
        else:
            context = {
                'error': form.errors
            }
            return render(request, 'order/address.html', context)
    else:
        return render(request, 'order/address.html')
