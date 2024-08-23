from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProdutorRural, Cultura
from .serializers import ProdutorRuralSerializer, CulturaSerializer

class ProdutorRuralViewSet(viewsets.ModelViewSet):
    queryset = ProdutorRural.objects.all()
    serializer_class = ProdutorRuralSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        culturas = CulturaSerializer(instance.cultura_set.all(), many=True)
        data = serializer.data
        data['culturas'] = culturas.data
        return Response(data)

    def create(self, request, *args, **kwargs):
        produtor_data = request.data
        culturas_data = produtor_data.pop('culturas', [])

        # Cria o Produtor Rural
        produtor_serializer = ProdutorRuralSerializer(data=produtor_data)
        if produtor_serializer.is_valid():
            produtor = produtor_serializer.save()

            # Cria as culturas associadas
            for cultura_data in culturas_data:
                cultura_data['produtor_rural'] = produtor.id
                cultura_serializer = CulturaSerializer(data=cultura_data)
                if cultura_serializer.is_valid():
                    cultura_serializer.save()
                else:
                    # Se houver um erro, desfaz a criação do produtor e culturas anteriores
                    produtor.delete()
                    return Response(cultura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(produtor_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(produtor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        produtor = self.get_object()
        produtor_data = request.data
        culturas_data = produtor_data.pop('culturas', [])

        # Atualiza o Produtor Rural
        produtor_serializer = ProdutorRuralSerializer(instance=produtor, data=produtor_data, partial=True)
        if produtor_serializer.is_valid():
            produtor = produtor_serializer.save()

            # Atualiza as culturas associadas
            Cultura.objects.filter(produtor_rural=produtor).delete()
            for cultura_data in culturas_data:
                cultura_data['produtor_rural'] = produtor.id                    
                cultura_serializer = CulturaSerializer(data=cultura_data)
                if cultura_serializer.is_valid():
                    cultura_serializer.save()
                else:
                    return Response(cultura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(produtor_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(produtor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CulturaViewSet(viewsets.ModelViewSet):
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer
