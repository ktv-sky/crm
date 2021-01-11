from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import admin_only, allowed_users, unauthenticated_user
from .filters import OrderFilter
from .forms import CreateUserForm, CustomerForm, OrderForm
from .models import Customer, Order, Product


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    return render(request, 'accounts/register.html', {
        'form': form
    })


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'accounts/login.html', {})


def logout_page(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {
        'products': products
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    return render(request, 'accounts/delete.html', {
        'item': order.product
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/user.html', {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):

    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    return render(request, 'accounts/account_settings.html', {
        'form': form
    })
