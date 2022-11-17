import email
from itertools import product
from random import choices
from tabnanny import verbose
from django.db import models
import datetime
import os
from django.contrib.auth.models import User
from PIL import Image



# Create your models here.

def get_file_path(request,filename):
    orginal_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime,orginal_filename)
    return os.path.join('uploads/',filename)


class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=get_file_path,null =True,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False, verbose_name=("0=default 1=Hidden"))
    trending = models.BooleanField(default=False, verbose_name=("0=default 1=Trending"))
    meta_title = models.CharField(max_length=150,blank=False)
    meta_keywords = models.CharField(max_length=150,blank=False)
    meta_description = models.TextField(max_length=150,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to=get_file_path,null =True,blank=False)
    image2 = models.ImageField(upload_to=get_file_path,null =False,blank=True)
    image3= models.ImageField(upload_to=get_file_path,null =False,blank=True)
    image4 = models.ImageField(upload_to=get_file_path,null =False,blank=True)
    image5 = models.ImageField(upload_to=get_file_path,null =False,blank=True)
    small_description = models.CharField(max_length=250,null=False,blank=False)
    SIZE_CHOICES = {
        ("S",'S'),
        ("M",'M'),
        ("L",'L'),
        ("XL",'XL'),
         ("XLL",'XLL'),
        ("XLLL",'XLLL'),
        
    }
    size = models.CharField(max_length=50,choices=SIZE_CHOICES,default='M')
    quantity = models.IntegerField(null=False,blank=False,default=25)
    description = models.TextField(max_length=500,null=False,blank=False)
    orginal_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    status = models.BooleanField(default=False, verbose_name=("0=default 1=Hidden"))
    trending = models.BooleanField(default=False, verbose_name=("0=default 1=Trending"))
    tag = models.CharField(max_length=150,null=False,blank=False)
    meta_title = models.CharField(max_length=150,blank=False)
    meta_keywords = models.CharField(max_length=150,blank=False)
    meta_description = models.TextField(max_length=150,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img1 = Image.open(self.image.path)
        if img1.height > 1500 or img1.width > 1500:
            output_size = (1500, 1500)
            img1.thumbnail(output_size)
            img1.save(self.image.path)

        if self.image2:
            img2 = Image.open(self.image2.path)
            if img2.height > 1500 or img2.width > 1500:
                output_size = (1500, 1500)
                img2.thumbnail(output_size)
                img2.save(self.image2.path)

        if self.image3:
            img3 = Image.open(self.image3.path)
            if img3.height > 1500 or img3.width > 1500:
                output_size = (1500, 1500)
                img3.thumbnail(output_size)
                img3.save(self.image3.path)

        if self.image4:
            img4 = Image.open(self.image4.path)
            if img4.height > 1500 or img4.width > 1500:
                output_size = (1500, 1500)
                img4.thumbnail(output_size)
                img4.save(self.image4.path)

        if self.image5:
            img5 = Image.open(self.image5.path)
            if img5.height > 1500 or img5.width > 1500:
                output_size = (1500, 1500)
                img5.thumbnail(output_size)
                img5.save(self.image5.path)

        
    def __str__(self):
        return self.name



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    time = models.DateTimeField(auto_now=True)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    SIZE_CHOICES = {
        ("S",'S'),
        ("M",'M'),
        ("L",'L'),
        ("XL",'XL'),
         ("XLL",'XLL'),
        ("XLLL",'XLLL'),
        
    }
    size = models.CharField(max_length=50,choices=SIZE_CHOICES,default='M')
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField( null=False)
    district = models.CharField(max_length=150,null=False)
    STATE_CHOICES = (
		("Andaman & Nicobar Islands",'Andaman & Nicobar Islands'),
		("Andhra Pradesh",'Andhra Pradesh'),
		("Arunachal Pradesh",'Arunachal Pradesh'),
		("Assam",'Assam'),
		("Bihar",'Bihar'),
		("Chandigarh",'Chandigarh'),
		("Chhattisgarh",'Chhattisgarh'),
		("Dadra & Nagar Haveli",'Dadra & Nagar Haveli'),
		("Daman and Diu",'Daman and Diu'),
		("Delhi",'Delhi'),
		("Goa",'Goa'),
		("Gujarat",'Gujarat'),
		("Haryana",'Haryana'),
		("Himachal Pradesh",'Himachal Pradesh'),
		("Jammu & Kashmir",'Jammu & Kashmir'),
		("Jharkhand",'Jharkhand'),
		("Karnataka",'Karnataka'),
		("Kerala",'Kerala'),
		("Lakshadweep",'Lakshadweep'),
		("Madhya Pradesh",'Madhya Pradesh'),
		("Maharashtra",'Maharashtra'),
		("Manipur",'Manipur'),
		("Meghalaya",'Meghalaya'),
		("Mizoram",'Mizoram'),
		("Nagaland",'Nagaland'),
		("Odisha",'Odisha'),
		("Puducherry",'Puducherry'),
		("Punjab",'Punjab'),
		("Rajasthan",'Rajasthan'),
		("Sikkim",'Sikkim'),
		("Tamil Nadu",'Tamil Nadu'),
		("Telangana",'Telangana'),
		("Tripura",'Tripura'),
		("Uttarakhand",'Uttarakhand'),
		("Uttar Pradesh",'Uttar Pradesh'),
		("West Bengal",'West Bengal'),
		)
	
    state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatuses = {
        ('Pending','Pending'),
        ('Out for Shipping','Out for Shipping'),
        ('Completed','Completed'),
    }
    status = models.CharField(max_length=150, choices=orderstatuses, default='Pending')
    message = models.TextField(null=True)
    tracking_id = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return ' {} - {}'.format(self.id,self.tracking_id)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    SIZE_CHOICES = {
        ("S",'S'),
        ("M",'M'),
        ("L",'L'),
        ("XL",'XL'),
         ("XLL",'XLL'),
        ("XLLL",'XLLL'),
        
    }
    size = models.CharField(max_length=50,choices=SIZE_CHOICES,default='M')
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    
    def __str__(self):
         return ' {} - {}'.format(self.order.id,self.order.tracking_id)
    
     
class Profile(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("store", self.user, instance)
        return None


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #image = models.ImageField(default='images/users.png', upload_to=image_upload_to)
    image = models.ImageField(default='static/images/users.png', upload_to='static/users',blank=True,null=True)

    phone = models.CharField(max_length=150, null=False)
    address = models.TextField( null=False)
    district = models.CharField(max_length=150,null=False)
    STATE_CHOICES = (
		("Andaman & Nicobar Islands",'Andaman & Nicobar Islands'),
		("Andhra Pradesh",'Andhra Pradesh'),
		("Arunachal Pradesh",'Arunachal Pradesh'),
		("Assam",'Assam'),
		("Bihar",'Bihar'),
		("Chandigarh",'Chandigarh'),
		("Chhattisgarh",'Chhattisgarh'),
		("Dadra & Nagar Haveli",'Dadra & Nagar Haveli'),
		("Daman and Diu",'Daman and Diu'),
		("Delhi",'Delhi'),
		("Goa",'Goa'),
		("Gujarat",'Gujarat'),
		("Haryana",'Haryana'),
		("Himachal Pradesh",'Himachal Pradesh'),
		("Jammu & Kashmir",'Jammu & Kashmir'),
		("Jharkhand",'Jharkhand'),
		("Karnataka",'Karnataka'),
		("Kerala",'Kerala'),
		("Lakshadweep",'Lakshadweep'),
		("Madhya Pradesh",'Madhya Pradesh'),
		("Maharashtra",'Maharashtra'),
		("Manipur",'Manipur'),
		("Meghalaya",'Meghalaya'),
		("Mizoram",'Mizoram'),
		("Nagaland",'Nagaland'),
		("Odisha",'Odisha'),
		("Puducherry",'Puducherry'),
		("Punjab",'Punjab'),
		("Rajasthan",'Rajasthan'),
		("Sikkim",'Sikkim'),
		("Tamil Nadu",'Tamil Nadu'),
		("Telangana",'Telangana'),
		("Tripura",'Tripura'),
		("Uttarakhand",'Uttarakhand'),
		("Uttar Pradesh",'Uttar Pradesh'),
		("West Bengal",'West Bengal'),
		)
	
    state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
