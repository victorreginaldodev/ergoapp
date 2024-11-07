from django.urls import path
from ordemServico.views.LiderTecnicoView import *

urlpatterns = [
    path('lider/', lider_tecnico, name='lider_tecnico'),
    path('tarefas/<int:servico_id>/', tarefas, name='tarefas'),
    path('lider/dashboard/lider', dashborad_lider, name='dashboard_lider'),
    path('api/servicos-por-status/', servicos_por_status, name='servicos_por_status'),
    path('conclusao_servicos_por_mes/', conclusao_servicos_por_mes, name='conclusao_servicos_por_mes'),
    path('lista_profiles/', lista_profiles, name='lista_profiles'),
    path('tarefas_por_status/', tarefas_por_status, name='tarefas_por_status'),  # Geral (sem filtro de profile)
    path('tarefas_por_status/<int:profile_id>/', tarefas_por_status, name='tarefas_por_status_profile'),  # Filtrado
]
