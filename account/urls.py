from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'
urlpatterns = [
    path('admin_dashboard/', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('customer_dashboard/', views.CustomerDashboard.as_view(), name='customer_dashboard'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('edit_product/<pk>/', views.EditProductView.as_view(), name='edit_product'),
    path('delete_product/<pk>/', views.delete_product, name='delete_product'),
    path('delete_customer/<pk>/', views.DeleteCustomerView.as_view(), name='delete_customer'),
    path('order_detail/<pk>/', views.CustomerOrderDetails.as_view(), name='order_detail'),
    path('change_password_customer/', views.CustomerChangePasswordView.as_view(), name='change_password_customer'),
    path("logout/", views.logout_user, name="logout"),
    # path("logout/", auth_views.LogoutView.as_view(next_page="/login/"), name="logout"),
]