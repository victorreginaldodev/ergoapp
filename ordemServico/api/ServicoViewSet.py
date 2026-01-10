from rest_framework import viewsets
from ordemServico.models import Servico
from ordemServico.serializers.ServicoSerializer import ServicoSerializer, ServicoListSerializer

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServicoListSerializer
        return ServicoSerializer
