# pedidos/urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('detalhes/<int:ped_conf_cli_ped_id>/', views.PedidoView.as_view(), name='pedido-detalhes'),
]
