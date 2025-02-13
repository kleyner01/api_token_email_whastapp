# custom_email/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('enviar/token/email/<int:ped_conf_cli_ped_id>/', views.EnviarEmailConfirmacaoPedido.as_view(), name='enviar-pedido-email'),
    path('confirmar/pedido/<str:token>/', views.ConfirmarPedidoAPI.as_view(), name='confirmar-pedido'),
]
