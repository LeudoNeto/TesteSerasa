from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from api.produtor_rural.models import ProdutorRural, Cultura

class DashboardAPIView(ViewSet):
    def list(self, request):
        total_fazendas = ProdutorRural.objects.count()

        total_hectares = ProdutorRural.objects.aggregate(Sum('area_total_hectares'))['area_total_hectares__sum'] or 0

        # Gráfico de pizza por estado
        estados = ProdutorRural.objects.values('estado').annotate(count=Count('id'))
        estados_pizza = {estado['estado']: estado['count'] for estado in estados}

        # Gráfico de pizza por cultura
        culturas = Cultura.objects.values('nome').annotate(count=Count('id'))
        culturas_pizza = {cultura['nome']: cultura['count'] for cultura in culturas}

        # Gráfico de pizza por uso de solo
        areas_agricultavel = ProdutorRural.objects.aggregate(Sum('area_agricultavel_hectares'))['area_agricultavel_hectares__sum'] or 0
        areas_vegetacao = ProdutorRural.objects.aggregate(Sum('area_vegetacao_hectares'))['area_vegetacao_hectares__sum'] or 0
        uso_solo_pizza = {
            'Agricultável': areas_agricultavel,
            'Vegetação': areas_vegetacao
        }

        # Montando a resposta
        data = {
            'total_fazendas': total_fazendas,
            'total_hectares': total_hectares,
            'estados_pizza': estados_pizza,
            'culturas_pizza': culturas_pizza,
            'uso_solo_pizza': uso_solo_pizza
        }

        return Response(data)
