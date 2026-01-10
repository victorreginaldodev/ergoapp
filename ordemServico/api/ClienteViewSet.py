from rest_framework import viewsets
from ordemServico.models import Cliente
from ordemServico.serializers.ClienteSerializer import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
