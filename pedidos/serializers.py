# pedidos/serializers.py
from rest_framework import serializers
from .models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    ped_conf_cli_dt_envio = serializers.DateTimeField(format="%d/%m/%Y - Hora: %H:%M:%S")
    ped_conf_cli_dt_lancto = serializers.DateTimeField(format="%d/%m/%Y - Hora: %H:%M:%S")
    ped_conf_cli_dt_confirmacao = serializers.DateTimeField(format="%d/%m/%Y - Hora: %H:%M:%S")

    class Meta:
        model = Pedido
        fields = '__all__'
