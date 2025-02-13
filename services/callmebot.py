from django.conf import settings
import requests
from urllib.parse import quote


class CallMeBot:

    def __init__(self):
        self.__base_url = settings.CALLMEBOT_API_URL
        self.__phone_number = settings.CALLMEBOT_PHONE_NUMBER
        self.__api_key = settings.CALLMEBOT_API_KEY

        if not self.__base_url or not self.__phone_number or not self.__api_key:
            raise ValueError("As configurações da API do CallMeBot não estão corretamente definidas no settings.py ou .env.")

    def send_message(self, message):
        encoded_message = quote(message)
        url = f'{self.__base_url}?phone={self.__phone_number}&text={encoded_message}&apikey={self.__api_key}'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.text
            else:
                return f"Erro na API: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Erro de rede: {str(e)}"
