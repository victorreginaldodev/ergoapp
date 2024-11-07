from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, F

from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

from ordemServico.models import Servico, Tarefa, Profile
from ordemServico.forms import ServicoUpdateForm, TarefaForm

# Função que verifica se o usuário é 'Diretor', 'Administrativo' ou 'Líder Técnico'
def verificar_tipo_usuario(user):
    try:
        return user.profile.role in [1, 2, 3]
    except Profile.DoesNotExist:
        return False

# Definindo o inlineformset_factory com os campos explicitamente
FormTarefaInlineFormset = inlineformset_factory(
    Servico,
    Tarefa,
    form=TarefaForm,
    fields=['profile', 'descricao'],
    extra=1
)

@user_passes_test(verificar_tipo_usuario)
@login_required
def lider_tecnico(request):
    # Filtra serviços com status 'em_espera'
    novos_servicos = Servico.objects.filter(status='em_espera')
    qtd_novos_servicos = novos_servicos.count()

    servicos_em_andamento = Servico.objects.annotate(
        total_tarefas=Count('tarefas'),
        tarefas_concluidas=Count('tarefas', filter=Q(tarefas__status='concluida'))
    ).filter(
        total_tarefas__gt=0,  # Certifica-se de que o serviço tenha tarefas
        tarefas_concluidas__lt=F('total_tarefas'),  # Verifica se nem todas as tarefas estão concluídas
        status='em_andamento'  # O status do serviço é 'em andamento'
    )
    qtd_servicos_em_andamento = servicos_em_andamento.count()

    # Filtra serviços concluídos
    servicos_finalizados = Servico.objects.filter(status='concluida')
    qtd_servicos_finalizados = servicos_finalizados.count()

    servicos_para_finalizar = Servico.objects.annotate(
        total_tarefas=Count('tarefas'),
        tarefas_concluidas=Count('tarefas', filter=Q(tarefas__status='concluida'))
    ).filter(
        total_tarefas__gt=0,
        total_tarefas=F('tarefas_concluidas'),
        status='em_andamento'
    )
    qtd_servicos_para_finalizar = servicos_para_finalizar.count()

    # Lógica para formulário de atualização de serviço
    if request.method == 'POST' and 'formUpdate' in request.POST:
        servico_id = request.POST.get('servico_id')
        servico = get_object_or_404(Servico, id=servico_id)
        formUpdate = ServicoUpdateForm(request.POST, instance=servico)

        if formUpdate.is_valid():
            formUpdate.save()
            messages.success(request, 'Serviço atualizado com sucesso.')
            return redirect('lider_tecnico')
        else:
            messages.error(request, 'Erro ao tentar atualizar o serviço.')
    else:
        formUpdate = ServicoUpdateForm()

    # Lógica para formulário de criação de tarefas
    if request.method == 'POST' and 'formTarefa' in request.POST:
        servico_id = request.POST.get('servico_id')
        servico = get_object_or_404(Servico, id=servico_id)
        form_tarefa = FormTarefaInlineFormset(request.POST, instance=servico)

        if form_tarefa.is_valid():
            form_tarefa.save()
            messages.success(request, 'Tarefas adicionadas com sucesso.')
            return redirect('lider_tecnico')
        else:
            messages.error(request, 'Erro ao tentar adicionar tarefas ao serviço.')
    else:
        servico_id = request.GET.get('servico_id')
        servico = get_object_or_404(Servico, id=servico_id) if servico_id else None
        form_tarefa = FormTarefaInlineFormset(instance=servico)

    context = {
        'novos_servicos': novos_servicos,
        'qtd_novos_servicos': qtd_novos_servicos,

        'servicos_em_andamento': servicos_em_andamento,
        'qtd_servicos_em_andamento': qtd_servicos_em_andamento,

        'servicos_finalizados': servicos_finalizados,
        'qtd_servicos_finalizados': qtd_servicos_finalizados,

        'servicos_para_finalizar': servicos_para_finalizar,
        'qtd_servicos_para_finalizar': qtd_servicos_para_finalizar,

        'formUpdate': formUpdate,
        'form_tarefa': form_tarefa,
    }

    return render(request, 'ordemServico/lider_tecnico.html', context)

@user_passes_test(verificar_tipo_usuario)
@login_required
def tarefas(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.servico = servico  # Aqui associamos o serviço
            tarefa.save()
            messages.success(request, 'Tarefa criada com sucesso.')
            return redirect('tarefas', servico_id=servico.id)
    else:
        form = TarefaForm()

    context = {
        'servico': servico,
        'form': form,
    }

    return render(request, 'ordemServico/tarefas.html', context)


@user_passes_test(verificar_tipo_usuario)
@login_required
def dashborad_lider(request):
    return render(request, 'ordemServico/area_tecnica/dashboard_lider.html')


STATUS_DISPLAY = {
    'em_espera': 'EM ESPERA',
    'em_andamento': 'EM ANDAMENTO',
    'concluida': 'CONCLUÍDA',
}

@user_passes_test(verificar_tipo_usuario)
@login_required
def servicos_por_status(request):
    contagem = Servico.objects.values('status').order_by('status').annotate(total=Count('id'))
    dados = {STATUS_DISPLAY[item['status']]: item['total'] for item in contagem}
    return JsonResponse(dados)


@user_passes_test(verificar_tipo_usuario)
@login_required
def conclusao_servicos_por_mes(request):
    # Define o intervalo de 6 meses a partir da data atual
    data_limite = timezone.now().date().replace(day=1) - timedelta(days=360) 

    # Filtra os serviços concluídos nos últimos 6 meses e agrupa por mês
    dados_conclusao = (
        Servico.objects
        .filter(status='concluida', data_conclusao__gte=data_limite)
        .annotate(mes_conclusao=TruncMonth('data_conclusao'))
        .values('mes_conclusao')
        .annotate(total=Count('id'))
        .order_by('mes_conclusao')
    )

    # Formata a data para "mês/ano" ao invés de "ano/mês"
    dados = {
        item['mes_conclusao'].strftime('%m/%Y'): item['total']
        for item in dados_conclusao
        if item['mes_conclusao']
    }
    return JsonResponse(dados)


@user_passes_test(verificar_tipo_usuario)
@login_required
def lista_profiles(request):
    profiles = Profile.objects.values('id', 'nome')
    return JsonResponse(list(profiles), safe=False)

@user_passes_test(verificar_tipo_usuario)
@login_required
def tarefas_por_status(request, profile_id=None):
    if profile_id:
        data = (
            Tarefa.objects.filter(profile_id=profile_id)
            .values('status')
            .annotate(total=Count('status'))
        )
    else:
        data = (
            Tarefa.objects
            .values('status')
            .annotate(total=Count('status'))
        )
    status_data = {item['status']: item['total'] for item in data}
    return JsonResponse(status_data)