# pedidos/models.py
from django.db import models
import uuid


class Pedido(models.Model):
    ped_conf_cli_id = models.IntegerField(db_column='ped_conf_cli_ID', primary_key=True)
    ped_conf_cli_ped_id = models.IntegerField(db_column='ped_conf_cli_PED_ID')
    ped_conf_cli_dt_envio = models.DateTimeField(db_column='ped_conf_cli_DT_ENVIO')
    ped_conf_cli_dt_confirmacao = models.DateTimeField(db_column='ped_conf_cli_DT_CONFIRMACAO', null=True)
    ped_conf_cli_token = models.CharField(max_length=36, default=uuid.uuid4)
    ped_conf_cli_sit_reg_id = models.IntegerField(db_column='ped_conf_cli_SIT_REG_ID')
    ped_conf_cli_dt_lancto = models.DateTimeField(db_column='ped_conf_cli_DT_LANCTO')

    class Meta:
        managed = False
        db_table = 'pedido_confirmacao_cliente'
        app_label = 'pedidos'

    def __str__(self):
        return f"Pedido Confirmação {self.ped_conf_cli_id} - Token: {self.ped_conf_cli_token}"
