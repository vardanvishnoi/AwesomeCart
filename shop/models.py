from django.db import models

# Create your models here.
class Product(models.Model):
            product_id=models.AutoField
            product_name=models.CharField(max_length=30)
            category=models.CharField(max_length=50,default="")
            sub_category=models.CharField(max_length=50,default="")
            price=models.IntegerField(default=0)
            desc=models.CharField(max_length=300)
            pub_date=models.DateField()
            image=models.ImageField(upload_to="shop/images",default="")
        
            def __str__(self):
                return self.product_name

class Contact(models.Model):
            msg_id=models.AutoField(primary_key="true")
            name=models.CharField(max_length=30)
            email=models.CharField(max_length=30,default="my@gmail.com") 
            phone=models.CharField(max_length=10)
            desc=models.TextField(max_length=500,default="")
        
            def __str__(self):
                return self.name
    
class Order(models.Model):
        order_id=models.AutoField(primary_key="true")
        items=models.CharField(max_length=5000,default="a")
        amount=models.IntegerField(default=0)
        name=models.CharField(max_length=30)
        email=models.CharField(max_length=30)
        phone=models.CharField(max_length=10)
        add=models.TextField(max_length=500,default="e")
        state=models.CharField(max_length=20)
        city=models.CharField(max_length=20)
        pin=models.CharField(max_length=10)
    
        def __str__(self):
            return self.name

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key="true")
    order_id=models.IntegerField(default=0)
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        strid=str(self.order_id)
        return strid

class UserDetail(models.Model):
    username=models.CharField(primary_key="true",max_length=30,default="")
    phone=models.CharField(max_length=10,default="")
    add=models.TextField(max_length=500,default="")
    state=models.CharField(max_length=20,default="")
    city=models.CharField(max_length=20,default="")
    pin=models.CharField(max_length=10,default="")
    userimage=models.ImageField(upload_to="userimage",default="/static/shop/icons/user.png")

    def __str__(self):
        return self.username
