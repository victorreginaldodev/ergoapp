from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
import locale

from ordemServico.models import Profile, Servico

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

    return render(request, 'ordemServico/painel_controle.html', context)