from django.urls import path
from django.views.decorators.cache import cache_page

from .views import detail, ProductsView

app_name = 'mainapp'

urlpatterns = [
   path('', ProductsView.as_view(), name='category'),
   path('category/<int:pk>', ProductsView.as_view(), name='category'),
   path('product/<int:pk>', detail, name='details'),
   path('category/<int:pk>/ajax', ProductsView.as_view()),
   path('category/<int:pk>?page=<int:page>)/ajax', ProductsView.as_view()),
]
