from django.contrib import admin

from .models import Customer, MyClient

admin.site.register(Customer)
admin.site.register(MyClient)
