from django.shortcuts import render


def shopcart(request):
    return render(request, 'cart/shopcart.html')
