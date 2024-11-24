from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from ordemServico.models import OrdemServico, Profile
from ordemServico.forms import OrdemServicoUpdateForm
from django.contrib import messages


def verificar_tipo_usuario(user):
    """
    Verifica se o usuário tem um papel permitido (Diretor, Administrativo ou Líder Técnico)
    """
    try:
        return user.profile.role in [1, 2, 3]
    except Profile.DoesNotExist:
        return False

@login_required
@user_passes_test(verificar_tipo_usuario)
def financeiro(request):
    ordens_servicos = OrdemServico.objects.all()

    # Lista de dicionários, cada um contendo uma ordem e seu formulário correspondente
    ordens_com_formularios = [
        {
            "ordem": ordem,
            "form": OrdemServicoUpdateForm(instance=ordem)
        }
        for ordem in ordens_servicos
    ]

    context = {
        "ordens_com_formularios": ordens_com_formularios,
        "total_faturadas": ordens_servicos.filter(faturamento="sim").aggregate(Sum("valor"))["valor__sum"] or 0,
        "total_liberadas": (
            OrdemServico.objects.filter(cobranca_imediata="sim", faturamento="nao") |
            OrdemServico.objects.filter(servicos__isnull=False, servicos__status="concluida")
            .exclude(faturamento="sim")
        ).distinct().aggregate(Sum("valor"))["valor__sum"] or 0,
        "total_nao_liberadas": sum(ordem.valor for ordem in ordens_servicos if not ordem.liberada_para_faturamento()),
    }

    return render(request, "ordemServico/financeiro/financeiro.html", context)
