from django.urls import path
from .views import detail, ProductsView

app_name = 'mainapp'

urlpatterns = [
   path('', ProductsView.as_view(), name='category'),
   path('category/<int:pk>', ProductsView.as_view(), name='category'),
   path('product/<int:pk>', detail, name='details'),
]
