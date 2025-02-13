# custom_email/serializers.py
from rest_framework import serializers
from .models import EmailRegistro


class EmailRegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRegistro
        fields = '__all__'
