from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    discount=models.IntegerField(default=0)
    file=models.FileField(upload_to='Upload/files',null=True,blank=True)
    thumbnail=models.ImageField(upload_to='Upload/thumbnail')
    link=models.CharField(max_length=200,null=True,blank=True)
    fileSize=models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product=models.ForeignKey(Product,default=None,on_delete=models.CASCADE,)
    image=models.ImageField(upload_to='Upload/images',blank=True)


class User(models.Model):
    name=models.CharField(max_length=100)
    active=models.BooleanField(default=True)
    email=models.CharField(max_length=100,unique=True,null=False,blank=False)
    password=models.CharField(max_length=500)
    phone=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Payment(models.Model):
    product=models.ForeignKey(Product,null=False,on_delete=models.CASCADE,)
    user=models.ForeignKey(User, null=False,on_delete=models.CASCADE,)
    payment_request_id=models.CharField(max_length=200,null=False,unique=True)
    payment_id=models.CharField(max_length=200)
    status=models.CharField(max_length=200,default="Failed")
    date=models.DateTimeField(auto_now_add=True)
