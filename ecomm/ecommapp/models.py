from django.db import models
from django.contrib.auth.models import User

#Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES=[
        (1,"Mobile"),
        (2,"Clothes"),
        (3,"Shoes")
    ]
    name=models.CharField(max_length=100) # is is use to name the product means table. here we have given a datatype and maximum length of the name
    price = models.FloatField()# we are adding the field in the table
    pdetails = models.CharField(max_length=300)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to='image')
    def __str__(self):
        return self.name

class Cart(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid = models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    order_id =models.CharField(max_length=100)
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid = models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    quantity = models.IntegerField(default=1)