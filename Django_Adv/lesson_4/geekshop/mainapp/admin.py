from django.contrib import admin
from .models import ProductCategories, Product
# Register your models here.

admin.site.register(ProductCategories)
admin.site.register(Product)
