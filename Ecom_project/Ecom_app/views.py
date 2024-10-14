from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework.authtoken.models import Token
import json
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import razorpay
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Creating Token while Registration by signal
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def generate_token(sender,instance,created=False,**kwarg):
    if created:
        Token.objects.create(user=instance)



class Create_Update_Delete_Product(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request):
        product_serialize = Product_Serializer(data=request.data)
        if product_serialize.is_valid():
            product_serialize.save()
            return Response({"product":"added successfully","data":product_serialize.data})
        return Response(product_serialize.errors)
    
    def put(self,request,pk):
        product = Product.objects.get(pk=pk)
        product_serialize = Product_Serializer(product,data=request.data)
        if product_serialize.is_valid():
            product_serialize.save()
            return Response("update succefully")
        return Response(product_serialize.errors)
        
    def delete(self,request,pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response("Product Deleted Successfully") 

import django_filters.rest_framework    
class Get_Product(APIView):
    def get(self,request):
        get_data = request.query_params
        if get_data:
            products = Product.objects.filter(price=get_data['price'])
        else:
            products = Product.objects.all()
            
        product_serialize = Product_Serializer(products,many=True)
        filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
        filterset_fields = ['name', 'price']
        return Response(product_serialize.data)
    
class Registe_User(APIView):
    def post(self,request):
        user_serialize = Register_User_Serializer(data=request.data)
        if user_serialize.is_valid():
            user_serialize.save()
            return Response("User registered successfully")
        return Response(user_serialize.errors)
    
    def get(self,request):
        get_user = User.objects.all()
        serialize_user = Register_User_Serializer(get_user,many=True)
        return Response(serialize_user.data)
    


class Get_Create_Update_Delete_Order(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # import pdb; pdb.set_trace()
        user = User.objects.get(username=request.user)
        all_order = OrderModel.objects.filter(user=user,is_cancelled=False,is_delivered=False)
        order_serialize = Order_Serializer(all_order,many=True)
        return Response(order_serialize.data)
    
    # def post(self,requset):
    #     order_serialize = Order_Serializer(data=requset.data)
    #     if order_serialize.is_valid():
    #         order_serialize.save()
    #         return Response({"Order Placed":order_serialize.data})
    #     return Response(order_serialize.errors)
    
    def delete(self,request,pk):
        # import pdb; pdb.set_trace()
        get_order=OrderModel.objects.get(id=pk)
        if get_order.is_refunded:
            return Response("Order Already Cancelled and refund initiated, will be refunded in 3-5 working days")
        if get_order.is_cancelled:
            return Response("Order Already Cancelled")
        if get_order.is_cashon:
            get_order.is_cancelled=True
            get_order.save()
            return Response("Order Cancel Successfully")
        get_order.save()
        get_pay_id = Payment_details.objects.get(order=get_order)
        amount = get_pay_id.price*100
        ##REFUND and CANCEL
        url = "https://api.razorpay.com/v1/payments/"+str(get_pay_id.pay_id)+"/refund"
        data = {
                "amount": amount,
                "currency": "INR",
                "speed":"optimum"
                }
        header= {'Authorization': 'Basic cnpwX3Rlc3RfcXU0MlJBanNnek04MHA6dlRCQXZ6S3pnZzFrZGhXMkc1Sk9MOU1L',
                'content-type': 'application/json',
                'Accept': 'application/json'}
        url_response = requests.post(url, json=data,headers=header)
        get_order.is_cancelled=True
        get_order.is_refunded=True
        get_order.save()
        return Response("Order Cancelled and Refund Initiated")
    
class Get_Create_Update_Delete_Address(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = User.objects.get(username=request.user)
        all_address = BillingAddress.objects.filter(user=user)
        address_serialize = BillingAddress_Serializer(all_address,many=True)
        return Response(address_serialize.data)
    
    def post(self,request):
        address_serialize = BillingAddress_Serializer(data=request.data)
        if address_serialize.is_valid():
            address_serialize.save()
            return Response({"status":"address added succefully","address":address_serialize.data})
        return Response(address_serialize.errors)

class Product_Cart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        Cart_detail=Cart_Order.objects.filter(user=request.user)
        serialize_cart = Cart_Serializer(Cart_detail,many=True)
        return Response(serialize_cart.data)
        
    def post(self,request):
        cart_serialize = Cart_Serializer(data=request.data)
        user = User.objects.get(username=request.user)
        if cart_serialize.is_valid():
            product_price = Product.objects.get(pk=cart_serialize.validated_data['product'].id)
            cart_serialize.validated_data['price']=product_price.price * cart_serialize.validated_data['quantity']
            cart_serialize.validated_data['user']=user
            cart_serialize.save()
            return Response("Product Added to Cart")
        return Response(cart_serialize.errors)
from django.db.models import Sum 
import requests

class Payment(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = User.objects.get(username=request.user)
        total_cart_value=Cart_Order.objects.filter(pk=user.id)
        # if total_cart_value.exists():
        q = Cart_Order.objects.aggregate(total=Sum("price"))
        url = "https://api.razorpay.com/v1/payment_links/"
        tot = q['total']*100
        data = {
                "amount": tot,
                "currency": "INR",
                "callback_url":"http://127.0.0.1:8000/Callback_fuc"
                # "expire_by": 1728650000 add timestamp of 15 min from current time 
                }
        header= {'Authorization': 'Basic cnpwX3Rlc3RfcXU0MlJBanNnek04MHA6dlRCQXZ6S3pnZzFrZGhXMkc1Sk9MOU1L',
                'content-type': 'application/json',
                'Accept': 'application/json'}
        url_response = requests.post(url, json=data,headers=header)
        print(url_response._content)
        _data = url_response._content
        _id =  json.loads(_data.decode('utf-8'))['id']
        _short_url =  json.loads(_data.decode('utf-8'))['short_url']
        Payment_details.objects.create(pay_link=_id,user=user)
        tot =tot//100
        return Response({"id":_id,"url":_short_url,"amount":tot})
        # return Response("Cart is Empty")

import datetime
from django.http import HttpResponse
class Callback_fuc(APIView):
    def get(self,request):
        if request.query_params['razorpay_payment_link_status']=="paid":
            user_from_paymane_detail = Payment_details.objects.get(pay_link=request.query_params['razorpay_payment_link_id'])
            user = User.objects.get(username=user_from_paymane_detail.user)
            cartt = Cart_Order.objects.filter(user=user)
            for cart in cartt:
                order=OrderModel.objects.create(ordered_item=cart.product,ordered_address=cart.address,user=user,paid_status=True,paid_at=datetime.datetime.now())
                order.save()
                Order_Tracking.objects.create(user=user,order=order)
                Payment_details.objects.create(pay_link=request.query_params['razorpay_payment_link_id'],order=order,user=user,pay_id=request.query_params['razorpay_payment_id'],price=cart.price)
            cartt.delete()
            return HttpResponse("Payment Done Succefully")
        
class CashOnDelivery(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = User.objects.get(username=request.user)
        cartt = Cart_Order.objects.filter(user=user)
        if cartt:
            for cart in cartt:
                order=OrderModel.objects.create(ordered_item=cart.product,ordered_address=cart.address,user=user,paid_status=True,paid_at=datetime.datetime.now())
                order.save()
                Order_Tracking.objects.create(user=user,order=order)
            cartt.delete()
            return Response({"order":"Placed succefully",
                            "payment":"Cash on delivery"})
        return Response("Cart is Empty")
    
class Deliverd_Item(APIView):
    def post(self,request):
        # import pdb; pdb.set_trace()
        serialize_data = Deliverd_Item_Serializer(data=request.data)
        if serialize_data.is_valid():
            get_order = OrderModel.objects.get(id=serialize_data.validated_data['order_id'])
            if get_order.is_delivered==False:
                get_track = Order_Tracking.objects.get(order=get_order.id)
                get_track.delete()
                get_order.is_delivered=True
                if get_order.is_cashon:
                    get_order.paid_at=datetime.datetime.now()
                    get_order.paid_status=True
                get_order.save()
                return Response("Order Delivered Succefully")
            return Response("Order Already Delivered")
        
class Update_Tracking_Status(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        track_serialize = Order_Tracking_Serializer(data=request.data)
        if track_serialize.is_valid():
            curr_hub = track_serialize.validated_data['Current_hub']
            get_order = OrderModel.objects.get(id=track_serialize.validated_data['order_id'])
            get_track = Order_Tracking.objects.get(order=get_order)
            get_track.current_hub=curr_hub
            get_track.save()
            return Response("Hub update succefully")
        return track_serialize.errors
    
    def get(self,request):
        user = User.objects.get(username=request.user)
        all_track = Order_Tracking.objects.filter(user=user)
        print(all_track)
        track_serialize = Get_Tracking_Serializer(all_track,many=True)
        return Response(track_serialize.data)
    
class Cancelled_Order(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = User.objects.get(username=request.user)
        get_orders = OrderModel.objects.filter(is_cancelled=True,user=user)
        order_serialize = Order_Serializer(get_orders,many=True)
        return Response(order_serialize.data)
