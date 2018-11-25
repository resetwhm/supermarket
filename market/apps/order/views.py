from django.shortcuts import render


def tureorder(request):
    return render(request, 'order/tureorder.html')
