from django.db.models import Q, Count, F, OuterRef, Subquery
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from ordemServico.models import OrdemServico, Servico
from ordemServico.serializers import (
    OrdemServicoSerializer,
    OrdemServicoListSerializer,
    OrdemServicoFaturamentoSerializer,
)

class OrdemServicoViewSet(viewsets.ModelViewSet): 
    queryset = OrdemServico.objects.select_related("cliente")
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrdemServicoListSerializer
        if self.action == 'faturamento':
            return OrdemServicoFaturamentoSerializer
        return OrdemServicoSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario_criador=self.request.user.username)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            print("\n\n========== ORDEM SERVICO UPDATE ERROR ==========")
            print(f"Request Data: {request.data}")
            print(f"Error Details: {e.detail}")
            print("================================================\n\n")
            raise e

    @action(detail=False, methods=['get'], url_path='faturamento')
    def faturamento(self, request):
        servicos_concluidos_subquery = (
            Servico.objects.filter(
                ordem_servico=OuterRef('pk'),
                status='concluida',
            )
            .values('ordem_servico')
            .annotate(count=Count('id'))
            .values('count')
        )

        total_servicos_subquery = (
            Servico.objects.filter(
                ordem_servico=OuterRef('pk'),
            )
            .values('ordem_servico')
            .annotate(count=Count('id'))
            .values('count')
        )

        annotated = self.get_queryset().annotate(
            total_servicos=Subquery(total_servicos_subquery),
            servicos_concluidos=Subquery(servicos_concluidos_subquery),
        )

        base_liberadas = annotated.filter(total_servicos=F('servicos_concluidos')).distinct()

        cobranca_imediata_qs = base_liberadas.filter(
            cobranca_imediata='sim',
            faturamento='nao',
        )

        servicos_concluidos_qs = (
            base_liberadas.filter(
                servicos__isnull=False,
                servicos__status='concluida',
            )
            .exclude(faturamento='sim')
        )

        queryset = (cobranca_imediata_qs | servicos_concluidos_qs).distinct()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
