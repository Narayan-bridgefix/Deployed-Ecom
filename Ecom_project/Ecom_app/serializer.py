from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User

class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class Order_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'
        
class Register_User_Serializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields =  ('username', 'password', 'first_name', 'last_name','email')
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class BillingAddress_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'
        
class Cart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Order
        fields = '__all__'
        
class Deliverd_Item_Serializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    
class Order_Tracking_Serializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    Current_hub = serializers.CharField()

class Get_Tracking_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Tracking
        fields = '__all__'