from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.http.response import JsonResponse


# Create your views here.

def home(request):
    return render(request, 'store/index.html')

def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category':category}
    return render(request, 'store/collections.html',context)

def collectionsview(request,name):
    if(Category.objects.filter(name=name, status=0)):
        products = Product.objects.filter(category__name=name)
        category = Category.objects.filter(name=name).first()
        context = {'products': products, 'category':category}
        return render(request,'store/products/index.html',context)
    else:
        messages.warning(request,"No such Category Found")
        return redirect('collections')
    
def productview(request,cate_name,prod_name):
    if(Category.objects.filter(name=cate_name,status=0)):
        if(Product.objects.filter(name=prod_name,status=0)):
            products = Product.objects.filter(name=prod_name,status=0).first()
            context = {'products':products}
            
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
        return redirect('collections')
    
    return render(request,'store/products/view.html',context)


def productlist(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productslist = list(products)
    
    return JsonResponse(productslist,safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searcheditem = request.POST.get('productsearch')
        if searcheditem == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains = searcheditem).first()
            
            if product:
                return redirect('collections/'+product.category.name+'/'+product.name)
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
                
            
    return redirect(request.META.get('HTTP_REFERER'))