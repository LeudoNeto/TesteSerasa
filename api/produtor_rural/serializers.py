from rest_framework import serializers
from .models import ProdutorRural, Cultura
from .utils import validate_cpf, validate_cnpj

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
        # Pega os valores antigos, para os casos de UPDATE ou PATCH
        instance = getattr(self, 'instance', None)

        usa_cpf = data.get('usa_cpf', getattr(instance, 'usa_cpf', None))
        cpf_cnpj = data.get('cpf_cnpj', getattr(instance, 'cpf_cnpj', None))
        area_agricultavel = data.get('area_agricultavel_hectares', getattr(instance, 'area_agricultavel_hectares', None))
        area_vegetacao = data.get('area_vegetacao_hectares', getattr(instance, 'area_vegetacao_hectares', None))
        area_total = data.get('area_total_hectares', getattr(instance, 'area_total_hectares', None))

        # Validação CPF/CNPJ
        if usa_cpf and not validate_cpf(cpf_cnpj):
            raise serializers.ValidationError("CPF inválido.")
        if not usa_cpf and not validate_cnpj(cpf_cnpj):
            raise serializers.ValidationError("CNPJ inválido")

        # Validação das áreas
        if area_agricultavel is not None and area_vegetacao is not None and area_total is not None:
            if area_agricultavel + area_vegetacao > area_total:
                raise serializers.ValidationError("A soma da área agricultável e da vegetação não pode ser maior que a área total da fazenda.")
        
        return data
