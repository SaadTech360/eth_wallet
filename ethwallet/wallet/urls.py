from django.urls  import path
from .views  import home,create_account,get_balance_url,send_transaction

urlpatterns = [
    path('',home,name='home'),
    path('create',create_account,name='create'),
    path('balance/<str:address>/',get_balance_url,name='get_balance'),
    path('send-transaction/',send_transaction,name='send'),
]