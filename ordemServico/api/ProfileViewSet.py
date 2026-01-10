from rest_framework import viewsets
from ordemServico.models import Profile
from ordemServico.serializers.ProfileSerializer import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

