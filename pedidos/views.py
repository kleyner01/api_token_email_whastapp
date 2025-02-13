# pedidos/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer


class PedidoView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_field = 'ped_conf_cli_ped_id'
