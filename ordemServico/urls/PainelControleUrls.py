from django.urls import path
from ordemServico.views.PainelControleView import painel_de_controle, servicos_graficos, detalhe_servico_modal

urlpatterns = [
    path('painel/', painel_de_controle, name='painel_de_controle'),
    path('servico/<int:servico_id>/', detalhe_servico_modal, name='servico'),
    path('api/servicos-graficos/', servicos_graficos, name='servicos_graficos'),
]