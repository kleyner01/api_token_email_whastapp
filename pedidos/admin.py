# pedidos/admin.py
from django.contrib import admin
from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'ped_conf_cli_id',
        'ped_conf_cli_ped_id',
        'ped_conf_cli_dt_envio',
        'ped_conf_cli_dt_confirmacao',
        'ped_conf_cli_token',
        'ped_conf_cli_sit_reg_id',
        'ped_conf_cli_dt_lancto',
    )

    list_filter = (
        'ped_conf_cli_dt_envio',
        'ped_conf_cli_dt_confirmacao',
        'ped_conf_cli_sit_reg_id',
    )

    search_fields = (
        'ped_conf_cli_id',
        'ped_conf_cli_ped_id',
    )

    readonly_fields = (
        'ped_conf_cli_id',
        'ped_conf_cli_dt_lancto',
        'ped_conf_cli_token',
        'ped_conf_cli_dt_envio',
        'ped_conf_cli_dt_confirmacao',
    )

    ordering = (
        '-ped_conf_cli_id',
        '-ped_conf_cli_ped_id',
        '-ped_conf_cli_dt_envio',
        '-ped_conf_cli_dt_confirmacao',
    )

    date_hierarchy = 'ped_conf_cli_dt_envio'

    # Remove ações de deletar e adicionar
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False  # Impede modificações nos objetos existentes

    def has_delete_permission(self, request, obj=None):
        return False  # Impede exclusões de objetos

    # Remove ações personalizadas (opcional)
    actions = None

    # Se desejar manter o método gerar_token_selecionados:
    # Adicione um if para verificar se a ação foi desativada
    def gerar_token_selecionados(self, request, queryset):
        self.message_user(request, "Ação desativada em modo somente leitura.")

    gerar_token_selecionados.short_description = "Ação desativada"
