from django.urls import path
import ordersapp.views as ordersapp


app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='order_list'),
    path('create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    path('update/<pk>', ordersapp.OrderUpdate.as_view(), name='order_update'),
    path('delete/<pk>', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('read/<pk>', ordersapp.OrderRead.as_view(), name='order_read'),
    path('forming/complete/<pk>', ordersapp.order_forming_complete, name='order_forming_complete'),
]


