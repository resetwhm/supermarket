from django.shortcuts import render

def index(request):
    return render(request,'goods/index.html')


def detail(request):
    return render(request,'goods/detail.html')


def category(request):
    return render(request,'goods/category.html')
