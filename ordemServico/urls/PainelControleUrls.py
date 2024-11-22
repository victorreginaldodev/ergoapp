from django.urls import path
from ordemServico.views.PainelControleView import painel_de_controle, servicos_graficos

urlpatterns = [
    path('painel/', painel_de_controle, name='painel_de_controle'),
    path('api/servicos-graficos/', servicos_graficos, name='servicos_graficos'),
]