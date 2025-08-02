from django.urls  import path
from .views  import create_account,get_balance,send_transaction

urlpatterns = [
    path('create',create_account,name='create'),
    path('balance/<str:addr>/',get_balance,name='get_balance'),
    path('send-transaction/',send_transaction,name='send'),
]