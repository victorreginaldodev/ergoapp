from rest_framework import serializers
from ordemServico.models import RepositorioMiniOS

class RepositorioMiniOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositorioMiniOS
        fields = '__all__'
