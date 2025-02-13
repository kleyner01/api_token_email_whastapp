# custom_email/models.py
from django.db import models
from pedidos.models import Pedido
from django.utils.timezone import now


class EmailRegistro(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='emails')
    email_enviado_para = models.EmailField()
    ped_conf_cli_dt_confirmacao = models.DateTimeField(db_column='ped_conf_cli_DT_CONFIRMACAO', null=True, default=now)

    def __str__(self):
        return f"E-mail para {self.email_enviado_para} em {self.ped_conf_cli_dt_confirmacao}"
