from django.urls import path
from ordemServico.views.OrdemServicoView import listar_ordens_servicos, criar_ordem_servico

urlpatterns = [
    path('criar/', criar_ordem_servico, name='criar_ordem_servico'),
    path('listar/ordens-servicos/', listar_ordens_servicos, name='listar_ordens_servicos'),
]
