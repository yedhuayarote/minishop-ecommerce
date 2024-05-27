from django.urls import path
from . import views

urlpatterns = [
    path('cartDetails', views.cart_details, name='cartDetails'),
    path('add/<int:product_id>/', views.add_cart, name='addcart'),
    path('minus/<int:product_id>/', views.min_cart, name='minus'),
    path('delete/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('payment', views.payment, name='payment'),
    path('successful', views.successful, name='successful'),


]
