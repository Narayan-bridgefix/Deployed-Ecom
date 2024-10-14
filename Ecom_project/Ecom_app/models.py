from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name + " id:- "+str(self.id)
    
    
class OrderModel(models.Model):
    ordered_item = models.ForeignKey("Product", on_delete=models.CASCADE)
    ordered_address = models.ForeignKey("BillingAddress", verbose_name=("Billing_adress"), on_delete=models.CASCADE,blank=True,null=True)
    paid_status = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_cashon = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    # price = models.IntegerField(default=0)
    # total_price = models.IntegerField(null=True, blank=True)
    # card_number = models.CharField(max_length=16, null=True, blank=True)
    # address = models.CharField(max_length=300, null=True, blank=True)
    # name = models.CharField(max_length=120)
    
class Cart_Order(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    address = models.ForeignKey("BillingAddress", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    
class BillingAddress(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, related_name="billingmodel", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    pin_code = models.CharField(max_length=6,  null=False, blank=False)
    house_no = models.CharField(max_length=300, null=False, blank=False)
    landmark = models.CharField(max_length=120, null=False, blank=False)
    city = models.CharField(max_length=120, null=False, blank=False)
    state = models.CharField(max_length=120,  null=False, blank=False)

    def __str__(self):
        return self.name
    
class Payment_details(models.Model):
    pay_link = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.ForeignKey("OrderModel", on_delete=models.CASCADE,null=True)
    price = models.IntegerField(default=0)
    pay_id = models.CharField(max_length=50,null=True)
    
class Order_Tracking(models.Model):
    order = models.ForeignKey("OrderModel", on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    current_hub = models.CharField( max_length=50,default="Waiting for courrier agent to pick-up") 