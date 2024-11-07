from django.urls import path
from ordemServico.views.LiderTecnicoView import *

urlpatterns = [
    path('lider/', lider_tecnico, name='lider_tecnico'),
    path('tarefas/<int:servico_id>/', tarefas, name='tarefas'),
    path('lider/dashboard/lider', dashborad_lider, name='dashboard_lider'),
    path('api/servicos-por-status/', servicos_por_status, name='servicos_por_status'),
]
