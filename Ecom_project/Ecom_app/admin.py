from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(BillingAddress)
admin.site.register(OrderModel)
admin.site.register(Cart_Order)
admin.site.register(Payment_details)
admin.site.register(Order_Tracking)