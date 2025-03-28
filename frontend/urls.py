from django.urls import path, include

from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('store/products/', views.AllProductView.as_view(), name='all_products'),
    path('store/product/details/<pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
]