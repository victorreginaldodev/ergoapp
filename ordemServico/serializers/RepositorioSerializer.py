from rest_framework import serializers
from ordemServico.models import Repositorio

class RepositorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repositorio
        fields = '__all__'
