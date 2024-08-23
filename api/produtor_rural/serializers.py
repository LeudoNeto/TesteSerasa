from rest_framework import serializers
from .models import ProdutorRural, Cultura
from .utils import validate_cpf, validate_cnpj

class CulturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultura
        fields = ['nome', 'produtor_rural']

class CulturaDoProdutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultura
        fields = ['nome']

class ProdutorRuralSerializer(serializers.ModelSerializer):
    culturas = CulturaDoProdutorSerializer(many=True, required=False)

    class Meta:
        model = ProdutorRural
        fields = [
            'id', 'cpf_cnpj', 'usa_cpf', 'nome', 'nome_fazenda',
            'cidade', 'estado', 'area_total_hectares', 
            'area_agricultavel_hectares', 'area_vegetacao_hectares',
            'culturas'
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
        if all(area is not None for area in [area_agricultavel, area_vegetacao, area_total]):
            if area_agricultavel + area_vegetacao > area_total:
                raise serializers.ValidationError("A soma da área agricultável e da vegetação não pode ser maior que a área total da fazenda.")
            
        # Validação e formatação do campo 'estado'
        estado = data.get('estado', '').strip().upper()
        if estado is not '':
            if not estado.isalpha() or len(estado) != 2:
                raise serializers.ValidationError("O campo 'estado' deve conter exatamente duas letras.")
            data['estado'] = estado
        
        return data
