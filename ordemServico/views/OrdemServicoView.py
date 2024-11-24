from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from ordemServico.forms import OrdemServicoForm, ServicoForm
from ordemServico.models import OrdemServico, Servico, Profile


def verificar_tipo_usuario(user):
    ''' 
        Função que verifica se o usuário é 'Diretor', 'Administrativo' ou 'Líder Técnico
    '''
    try:
        return user.profile.role in [1, 2, 3]
    except Profile.DoesNotExist:
        return False

@login_required
@user_passes_test(verificar_tipo_usuario)
def criar_ordem_servico(request):
    ServicoFormSet = inlineformset_factory(
        OrdemServico,
        Servico,
        form=ServicoForm,
        extra=1
    )

    if request.method == 'POST':
        ordem_servico_form = OrdemServicoForm(request.POST)
        servico_formset = ServicoFormSet(request.POST)

        if ordem_servico_form.is_valid() and servico_formset.is_valid():
            # Salva a Ordem de Serviço e associa o usuário criador
            ordem_servico = ordem_servico_form.save(commit=False)
            ordem_servico.usuario_criador = request.user.username
            ordem_servico.save()

            # Associa os serviços à Ordem de Serviço criada
            servico_formset.instance = ordem_servico
            servico_formset.save()

            messages.success(request, "Ordem de Serviço criada com sucesso!")
            return redirect(reverse('criar_ordem_servico'))
        else:
            # Mensagens de erro para formulário inválido
            if not ordem_servico_form.is_valid():
                messages.error(request, "Erro ao salvar a Ordem de Serviço. Verifique os campos.")
            if not servico_formset.is_valid():
                messages.error(request, "Erro ao salvar os serviços. Verifique os campos.")
            
            context = {
                'ordem_servico_form': ordem_servico_form,
                'servico_formset': servico_formset,
            }
            return render(request, 'ordemServico/ordem_servico/ordem_servico.html', context)

    else:
        ordem_servico_form = OrdemServicoForm()
        servico_formset = ServicoFormSet()

        context = {
            'ordem_servico_form': ordem_servico_form,
            'servico_formset': servico_formset,
        }
        return render(request, 'ordemServico/ordem_servico/ordem_servico.html', context)