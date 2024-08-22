from rest_framework import serializers
from .models import ProdutorRural, Cultura

class CulturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultura
        fields = ['nome', 'produtor_rural']

class ProdutorRuralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutorRural
        fields = [
            'id', 'cpf_cnpj', 'usa_cpf', 'nome', 'nome_fazenda',
            'cidade', 'estado', 'area_total_hectares', 
            'area_agricultavel_hectares', 'area_vegetacao_hectares',
        ]
