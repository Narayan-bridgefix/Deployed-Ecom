from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('product/',Create_Update_Delete_Product.as_view()),
    path('product-list/',Get_Product.as_view()),
    path('product-UpdateorDelete/<int:pk>/',Create_Update_Delete_Product.as_view()),
    path('Registration/',Registe_User.as_view()),
    path('order/',Get_Create_Update_Delete_Order.as_view()),
    path('order-UpdateOrCancle/<int:pk>/',Get_Create_Update_Delete_Order.as_view()),
    path('adress/',Get_Create_Update_Delete_Address.as_view()),
    path('cart/',Product_Cart.as_view()),
    path('payment/',Payment.as_view()),
    path('Callback_fuc/',Callback_fuc.as_view()),
    path('COD/',CashOnDelivery.as_view()),
    path('delivered_item/',Deliverd_Item.as_view()),
    path('update_tracking/',Update_Tracking_Status.as_view()),
    path('order-cancelled/',Cancelled_Order.as_view()),
    path('order-delivered/',Delivered_Order.as_view()),

]

#configure for static files
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)