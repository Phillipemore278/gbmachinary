from django.urls import path, include

from . import views

app_name = 'order'
urlpatterns = [
    path('edit_order/<pk>/', views.EditOrderView.as_view(), name='edit_order'),
    path('delete_order/<pk>/', views.delete_order, name='delete_order'),
    path('view_receipt/<pk>/', views.view_receipt, name='view_receipt'),
]