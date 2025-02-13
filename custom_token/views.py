# token/views.py
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from pedidos.models import Pedido
from pedidos.serializers import PedidoSerializer
import uuid


class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, ped_conf_cli_ped_id):
        try:
            # Tenta buscar o pedido pelo ped_conf_cli_ped_id
            pedido = Pedido.objects.get(ped_conf_cli_ped_id=ped_conf_cli_ped_id)

            # Verifica se já existe um token
            if pedido.ped_conf_cli_token:
                return Response({
                    "mensagem": "Token já gerado",
                    "token": pedido.ped_conf_cli_token
                }, status=status.HTTP_200_OK)

            # Se não houver token, gera um novo
            pedido.ped_conf_cli_token = str(uuid.uuid4())  # Gera um UUID único como token
            pedido.ped_conf_cli_dt_envio = timezone.now()  # Atualiza a data de envio com a data atual
            pedido.save()  # Salva as alterações no banco

            # Serializa os dados para retornar como resposta
            serializer = PedidoSerializer(pedido)
            return Response({
                "mensagem": "Token gerado com sucesso",
                "dados": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Pedido.DoesNotExist:
            return Response(
                {"error": "Pedido não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
