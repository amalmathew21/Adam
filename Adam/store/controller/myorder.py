from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Order, OrderItem

def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,'store/orders/index.html', context)

def vieworder(request, t_id):
    order = Order.objects.filter(tracking_id=t_id).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderitems }
    return render(request, 'store/orders/view.html',context)
    