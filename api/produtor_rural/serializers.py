from rest_framework import serializers
from .models import ProdutorRural, Cultura
from .utils import valida_cpf, valida_cnpj

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

    def validate(self, data):
        if data['usa_cpf'] and not valida_cpf(data['cpf_cnpj']):
            raise serializers.ValidationError("CPF inválido.")

        if not data['usa_cpf'] and not valida_cnpj(data['cpf_cnpj']):
            raise serializers.ValidationError("CNPJ inválido")

        if data['area_agricultavel_hectares'] + data['area_vegetacao_hectares'] > data['area_total_hectares']:
            raise serializers.ValidationError("A soma da área agricultável e da vegetação não pode ser maior que a área total da fazenda.")
        return data
