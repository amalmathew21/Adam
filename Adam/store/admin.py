from django.contrib import admin
from .models import Cart, Category, OrderItem,Product,ProductReview,Order, Profile,Wishlist


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(ProductReview)
admin.site.register(Cart)
admin.site.register(Wishlist)
