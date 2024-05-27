from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('blog', views.blog, name='blog'),
    path('forgotpassword', views.forgot_password, name='forgotpassword'),
    path('password_reset/done/', views.password_reset_done, name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name="password_reset_confirm"),
    path('reset/done/', views.password_reset_complete, name="password_reset_complete"),
]



