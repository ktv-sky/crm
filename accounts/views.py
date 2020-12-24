from django.shortcuts import render

from .models import Product, Customer, Order, Tag


def home(request):
    return render(request, 'accounts/dashboard.html')


def products(request):
    return render(request, 'accounts/products.html', {
        'products': Product.objects.all()
    })


def customer(request):
    return render(request, 'accounts/customer.html')
