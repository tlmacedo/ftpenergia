from django.urls import path

from energia.models import *
from energia.views import LeiturasListView, LeituraCreateView

app_name = 'energia'

urlpatterns = [
    path('', LeiturasListView.as_view(), name='leitura_lista'),
    path('leitura_adicionar/', LeituraCreateView.as_view(), name='leitura_adicionar'),
]
