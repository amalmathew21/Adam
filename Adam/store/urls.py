
from django.urls import path
from .import views

from store.controller import authview, cart, wishlist, checkout, myorder

urlpatterns = [
    path('',views.home,name='home'),
    path('collections',views.collections, name='collections'),
    path('collections/<str:name>',views.collectionsview, name='collectionsview'),
    path('collections/<str:cate_name>/<str:prod_name>',views.productview,name='productview'),
    
    path('register/',authview.register, name='register'),
    path('login/',authview.loginpage,name='loginpage'),
    path('logout/',authview.logoutpage,name='logoutpage'),
    
    path('add-to-cart',cart.addtocart,name='addtocart'),
    path('cart',cart.viewcart,name='cart'),
    path('update-cart',cart.updatecart, name='updatecart'),
    path('delete-cart-item',cart.deletecartitem, name='deletecartitem'),
    
    path('wishlist',wishlist.index, name='wishlist'),
    path('add-to-wishlist',wishlist.addtowishlist, name='add-to-wishlist'),
    path('delete-wishlist-item',wishlist.deletewishlistitem, name='deletewishlistitem'),
    
    path('checkout',checkout.index,name='checkout'),
    path('place-order',checkout.placeorder,name='placeorder'),
    
    path('proceed-to-pay', checkout.razorpaycheck),
    path('my-orders', myorder.index, name="myorders"),
    path('view-order/<str:t_id>',myorder.vieworder, name="orderview"),
    
    path('product-list',views.productlist),
    path('search-products',views.searchproduct,name='search-products'),
    
    
    
]