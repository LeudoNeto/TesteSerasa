from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.produtor_rural.models import ProdutorRural, Cultura

class DashboardAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Criar dados de exemplo para ProdutorRural
        ProdutorRural.objects.create(
            cpf_cnpj='12345678901',
            usa_cpf=True,
            nome='Produtor 1',
            nome_fazenda='Fazenda 1',
            cidade='Cidade A',
            estado='SP',
            area_total_hectares=100.00,
            area_agricultavel_hectares=60.00,
            area_vegetacao_hectares=40.00
        )
        ProdutorRural.objects.create(
            cpf_cnpj='10987654321',
            usa_cpf=True,
            nome='Produtor 2',
            nome_fazenda='Fazenda 2',
            cidade='Cidade B',
            estado='GO',
            area_total_hectares=200.00,
            area_agricultavel_hectares=150.00,
            area_vegetacao_hectares=50.00
        )
        
        # Criar dados de exemplo para Cultura
        Cultura.objects.create(nome='Soja', produtor_rural=ProdutorRural.objects.first())
        Cultura.objects.create(nome='Milho', produtor_rural=ProdutorRural.objects.first())
        Cultura.objects.create(nome='Soja', produtor_rural=ProdutorRural.objects.last())

    def test_dashboard_endpoint(self):
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Verificar se o total de fazendas está correto
        self.assertEqual(data['total_fazendas'], 2)

        # Verificar se o total de hectares está correto
        self.assertEqual(data['total_hectares'], 300.00)

        # Verificar os estados para gráfico de pizza
        self.assertEqual(data['estados_pizza'], {'SP': 1, 'GO': 1})

        # Verificar as culturas para gráfico de pizza
        self.assertEqual(data['culturas_pizza'], {'Soja': 2, 'Milho': 1})

        # Verificar o uso de solo para gráfico de pizza
        self.assertEqual(data['uso_solo_pizza'], {'Agricultável': 210.00, 'Vegetação': 90.00})
