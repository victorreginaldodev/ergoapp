from rest_framework import viewsets
from ordemServico.models import MiniOS
from ordemServico.serializers import MiniOSSerializer

class MiniOsViewSet(viewsets.ReadOnlyModelViewSet):  # Certifique-se de usar a classe correta
    queryset = MiniOS.objects.all()
    serializer_class = MiniOSSerializer
