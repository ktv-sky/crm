from django.shortcuts import get_object_or_404, render

from .models import Product, Customer, Order, Tag


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    })


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products': products
    })


def customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    orders = customer.order_set.all()

    return render(request, 'accounts/customer.html', {
        'customer': customer,
        'orders': orders,
    })
