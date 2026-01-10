from rest_framework import viewsets
from ordemServico.models import Repositorio
from ordemServico.serializers.RepositorioSerializer import RepositorioSerializer

class RepositorioViewSet(viewsets.ModelViewSet):
    queryset = Repositorio.objects.all()
    serializer_class = RepositorioSerializer
