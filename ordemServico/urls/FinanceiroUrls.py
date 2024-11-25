from django.urls import path
from ordemServico.views.FinanceiroView import financeiro, salvar_ordem_servico, atualizar_contador_liberadas
urlpatterns = [
    path('financeiro/', financeiro, name='financeiro'),
    path("salvar-ordem-servico/", salvar_ordem_servico, name="salvar_ordem_servico"),
    path("atualizar-contador-liberadas/", atualizar_contador_liberadas, name="atualizar_contador_liberadas"),
]
