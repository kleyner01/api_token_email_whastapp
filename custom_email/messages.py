# custom_email/messages.py

def formatar_mensagem_whatsapp(pedido, link_confirmacao):
    """
    Função para formatar a mensagem de confirmação para WhatsApp.
    """
    return f"""
    Pedido de Confirmação:

    ID do Pedido: {pedido.ped_conf_cli_ped_id}
    Token de Autenticação: {pedido.ped_conf_cli_token}
    Data de Envio: {pedido.ped_conf_cli_dt_envio.strftime('%d/%m/%Y %H:%M:%S')}

    Link de Confirmação: {link_confirmacao}
    """
