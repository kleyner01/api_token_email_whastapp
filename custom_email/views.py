# custom_email/views.py

# Importações de bibliotecas do Django e REST Framework
from rest_framework import status  # Para definir códigos de status HTTP nas respostas
from rest_framework.views import APIView  # Base para criar views baseadas em classes
from rest_framework.response import Response  # Para retornar respostas estruturadas JSON
from rest_framework.permissions import AllowAny  # Permissão para acesso irrestrito à view
from django.core.mail import EmailMultiAlternatives  # Para enviar e-mails com múltiplos formatos (texto e HTML)
from email.mime.image import MIMEImage  # Para anexar imagens ao e-mail
from django.conf import settings  # Para acessar configurações globais do projeto
from django.utils import timezone  # Para manipular datas e horários
from django.urls import reverse  # Para gerar URLs dinamicamente a partir de nomes de rota
from django.contrib.sites.shortcuts import get_current_site  # Para obter o domínio atual do site

# Importações específicas do app
from pedidos.models import Pedido  # Modelo relacionado a pedidos
from pedidos.serializers import PedidoSerializer  # Serializador para transformar objetos `Pedido` em JSON

# Bibliotecas adicionais
import uuid  # Para gerar tokens únicos
from django.template.loader import render_to_string  # Para renderizar templates HTML
from django.shortcuts import render  # Para renderizar páginas HTML
from services.callmebot import CallMeBot
from .messages import formatar_mensagem_whatsapp


# Classe para envio de e-mail de confirmação de pedido
class EnviarEmailConfirmacaoPedido(APIView):
    permission_classes = [AllowAny]

    def post(self, request, ped_conf_cli_ped_id):
        """
        Este método recebe um ID de pedido, verifica se ele já foi confirmado,
        e, caso não tenha sido, envia um e-mail ao cliente com um link de confirmação.
        """
        try:
            # Obtém o pedido pelo ID fornecido
            pedido = Pedido.objects.get(ped_conf_cli_ped_id=ped_conf_cli_ped_id)

            # Verifica se o pedido já foi confirmado
            if pedido.ped_conf_cli_dt_confirmacao:
                return Response({
                    'message': f'O pedido já foi confirmado na data {pedido.ped_conf_cli_dt_confirmacao.strftime("%d/%m/%Y %H:%M:%S")}.',
                    'pedido_id': pedido.ped_conf_cli_ped_id,
                    'pedido_detalhes': PedidoSerializer(pedido).data
                }, status=status.HTTP_200_OK)

            # Gera um token único se ainda não houver
            if not pedido.ped_conf_cli_token:
                pedido.ped_conf_cli_token = str(uuid.uuid4()).upper()
                pedido.ped_conf_cli_dt_envio = timezone.now()
                pedido.save()

            # Gera o link de confirmação
            site = get_current_site(request)
            link_confirmacao = f"http://{site.domain}{reverse('confirmar-pedido', kwargs={'token': pedido.ped_conf_cli_token.upper()})}"

            mensagem_whatsapp = formatar_mensagem_whatsapp(pedido, link_confirmacao)

            # Contexto para renderizar o e-mail
            context = {
                'email': request.data.get('email'),
                'pedido': pedido,
                'link_confirmacao': link_confirmacao
            }
            html_mensagem = render_to_string('corpo_email.html', context)

            # Configuração do e-mail
            email = EmailMultiAlternatives(
                subject='Confirmação de Pedido',
                body="",
                from_email=settings.EMAIL_HOST_USER,
                to=[request.data.get('email')],
            )
            email.attach_alternative(html_mensagem, "text/html")

            # Anexa uma imagem ao e-mail
            with open('static/img/email.png', 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<evento_image>')
                img.add_header('Content-Disposition', 'inline')
                email.attach(img)

            # Envia o e-mail
            email.send(fail_silently=False)

            # Agora, envia a mensagem via WhatsApp
            callmebot = CallMeBot()
            response_message = callmebot.send_message(mensagem_whatsapp)

            if "Erro" in response_message:
                return Response({"error": f"Erro ao enviar mensagem WhatsApp: {response_message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Responde ao cliente após e-mail e WhatsApp serem enviados
            return Response({
                'message': 'E-mail e mensagem WhatsApp enviados com sucesso',
                'pedido_id': pedido.ped_conf_cli_ped_id
            }, status=status.HTTP_200_OK)

        except Pedido.DoesNotExist:
            # Retorna um erro se o pedido não existir
            return Response({'error': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)


# Classe para confirmar o pedido usando o token fornecido
class ConfirmarPedidoAPI(APIView):
    """
    Esta view permite confirmar pedidos usando um token único.
    """
    # Métodos GET e POST redirecionam para o mesmo método de confirmação
    def get(self, request, token):
        return self.confirmar_pedido(request, token)

    def post(self, request, token):
        return self.confirmar_pedido(request, token)

    def confirmar_pedido(self, request, token):
        """
        Realiza a confirmação do pedido se o token for válido e não utilizado previamente.
        """
        if not token.upper():
            return Response({'error': 'Token não informado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Busca o pedido pelo token
            pedido = Pedido.objects.get(ped_conf_cli_token=token)

            # Verifica se o pedido já foi confirmado
            if pedido.ped_conf_cli_dt_confirmacao:
                return render(request, 'confirmation.html', {
                    'already_confirmed': True,
                    'pedido': pedido,
                    'confirmation_date': pedido.ped_conf_cli_dt_confirmacao.strftime("%d/%m/%Y às %H:%M:%S")
                })

            # Confirmação normal
            pedido.ped_conf_cli_dt_confirmacao = timezone.now()
            pedido.save()

            html_mensagem = render_to_string('confirmation.html', {
                'success': True,
                'pedido': pedido
            })

            # Configuração do e-mail
            email = EmailMultiAlternatives(
                subject='Confirmação de Pedido',
                body="",
                from_email=settings.EMAIL_HOST_USER,
                to=[request.data.get('email')],
            )
            email.attach_alternative(html_mensagem, "text/html")

            # Anexa uma imagem ao e-mail
            with open('static/img/email.png', 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<evento_image>')
                img.add_header('Content-Disposition', 'inline')
                email.attach(img)

            # Envia o e-mail
            email.send(fail_silently=False)

            return render(request, 'confirmation.html', {
                'success': True,
                'pedido': pedido
            })

        except Pedido.DoesNotExist:
            # Retorna uma página de erro se o pedido não for encontrado
            return render(request, 'confirmation.html', {
                'error': True,
                'message': 'Pedido não encontrado'
            })
