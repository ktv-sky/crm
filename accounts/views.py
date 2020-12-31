from django.shortcuts import get_object_or_404, redirect, render

from .filters import OrderFilter
from .forms import OrderForm
from .models import Customer, Order, Product


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


def customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    orders = customer.order_set.all()
    order_count = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    return render(request, 'accounts/customer.html', {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'my_filter': my_filter
    })


def create_order(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'accounts/order_form.html', {
        'form': form,
        'customer': customer
    })


def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method != 'POST':
        form = OrderForm(instance=order)
    else:
        form = OrderForm(data=request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')


    return render(request, 'accounts/order_form.html', {
        'form': form
    })


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    return render(request, 'accounts/delete.html', {
        'item': order.product
    })
