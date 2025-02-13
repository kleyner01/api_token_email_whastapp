# token/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('token/<int:ped_conf_cli_ped_id>/', views.TokenView.as_view(), name='token'),
]
