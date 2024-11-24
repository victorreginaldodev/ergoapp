from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
import locale

from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

from ordemServico.models import Profile, OrdemServico, Servico

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def verificar_tipo_usuario(user):
    try:
        return user.profile.role in [1, 2, 3]
    except Profile.DoesNotExist:
        return False

@login_required
@user_passes_test(verificar_tipo_usuario)
def painel_de_controle(request):
    # Todos os serviços
    servicos = Servico.objects.all().order_by('-ordem_servico__data_criacao')

    context = {
        'servicos': servicos,
    }

    return render(request, 'ordemServico/painel_controle/painel_controle.html', context)


@login_required
@user_passes_test(verificar_tipo_usuario)
def detalhe_servico_modal(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    data = {
        'cliente': servico.ordem_servico.cliente.nome,
        'servico': servico.repositorio.nome,
        'data_recebimento': servico.ordem_servico.data_criacao.strftime('%d/%m/%Y'),
        'data_conclusao': servico.data_conclusao.strftime('%d/%m/%Y') if servico.data_conclusao else None,
        'status': servico.get_status_display(),
        'descricao': servico.descricao,
    }
    return JsonResponse(data)

def servicos_graficos(request):
    # 1. Quantidade de serviços criados por mês
    servicos_por_mes = (
        Servico.objects.filter(ordem_servico__data_criacao__isnull=False)
        .annotate(mes=TruncMonth('ordem_servico__data_criacao'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    # 2. Quantidade de serviços por status
    servicos_por_status = (
        Servico.objects.values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )

    # 3. Valor de vendas por mês
    vendas_por_mes = (
        OrdemServico.objects.filter(data_criacao__isnull=False)
        .annotate(mes=TruncMonth('data_criacao'))
        .values('mes')
        .annotate(total_vendas=Sum('valor'))
        .order_by('mes')
    )

    # Converte os dados para listas para serem enviados como JSON
    servicos_por_mes = list(servicos_por_mes)
    servicos_por_status = list(servicos_por_status)
    vendas_por_mes = list(vendas_por_mes)

    # Retorna os dados como JSON
    return JsonResponse({
        'servicos_por_mes': servicos_por_mes,
        'servicos_por_status': servicos_por_status,
        'vendas_por_mes': vendas_por_mes,
    })
