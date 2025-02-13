# custom_email/serializers.py
from rest_framework import serializers
from .models import EmailRegistro


class EmailRegistroSerializer(serializers.ModelSerializer):
    ped_conf_cli_dt_confirmacao = serializers.DateTimeField(format="%d/%m/%Y - Hora: %H:%M:%S")

    class Meta:
        model = EmailRegistro
        fields = '__all__'
