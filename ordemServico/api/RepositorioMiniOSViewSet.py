from rest_framework import viewsets
from ordemServico.models import RepositorioMiniOS
from ordemServico.serializers.RepositorioMiniOSSerializer import RepositorioMiniOSSerializer

class RepositorioMiniOSViewSet(viewsets.ModelViewSet):
    queryset = RepositorioMiniOS.objects.all()
    serializer_class = RepositorioMiniOSSerializer
