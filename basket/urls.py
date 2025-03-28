from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'basket'
urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('basket_add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('checkout_order/', views.checkout_order, name='checkout_order'),
    path('order_successful/', views.order_successful, name='order_successful'),
]