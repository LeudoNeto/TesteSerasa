from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProdutorRural, Cultura
from .serializers import ProdutorRuralSerializer, CulturaSerializer

class ProdutorRuralViewSet(viewsets.ModelViewSet):
    queryset = ProdutorRural.objects.all()
    serializer_class = ProdutorRuralSerializer

    @action(detail=False, methods=['post'], url_path='create_with_cultures')
    def create_with_cultures(self, request):
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
                    print('salvou', cultura_serializer.data)
                else:
                    print('houve erro')
                    # Se houver um erro, desfaz a criação do produtor e culturas anteriores
                    produtor.delete()
                    return Response(cultura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(produtor_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(produtor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CulturaViewSet(viewsets.ModelViewSet):
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer
