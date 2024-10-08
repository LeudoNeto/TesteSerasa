from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ProdutorRural, Cultura

class ProdutorRuralAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_cpf = "123.456.789-09"
        self.invalid_cpf = "123.456.789-00"
        self.valid_cnpj = "12.345.678/0001-95"
        self.invalid_cnpj = "12.345.678/0001-00"

        self.produtor_rural_data = {
            "cpf_cnpj": self.valid_cpf,
            "usa_cpf": True,
            "nome": "João Silva",
            "nome_fazenda": "Fazenda Silva",
            "cidade": "Fortaleza",
            "estado": "CE",
            "area_total_hectares": 100.00,
            "area_agricultavel_hectares": 50.00,
            "area_vegetacao_hectares": 30.00,
        }

    def test_create_produtor_rural_with_valid_cpf(self):
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_produtor_rural_with_invalid_cpf(self):
        self.produtor_rural_data["cpf_cnpj"] = self.invalid_cpf
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("CPF inválido.", response.data['non_field_errors'])

    def test_create_produtor_rural_with_valid_cnpj(self):
        self.produtor_rural_data.update({
            "cpf_cnpj": self.valid_cnpj,
            "usa_cpf": False,
        })
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_produtor_rural_with_invalid_cnpj(self):
        self.produtor_rural_data.update({
            "cpf_cnpj": self.invalid_cnpj,
            "usa_cpf": False,
        })
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("CNPJ inválido", response.data['non_field_errors'])

    def test_create_produtor_rural_with_excessive_agricultural_area(self):
        self.produtor_rural_data.update({
            "area_agricultavel_hectares": 60.00,
            "area_vegetacao_hectares": 50.00,
        })
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A soma da área agricultável e da vegetação não pode ser maior que a área total da fazenda.", response.data['non_field_errors'])

    def test_create_produtor_rural_with_valid_data(self):
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProdutorRural.objects.count(), 1)
        self.assertEqual(ProdutorRural.objects.get().nome, 'João Silva')

    def test_create_cultura_for_produtor_rural(self):
        produtor = ProdutorRural.objects.create(**self.produtor_rural_data)
        cultura_data = {
            "nome": "Soja",
            "produtor_rural": produtor.id
        }
        response = self.client.post('/api/cultura/', cultura_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cultura.objects.count(), 1)
        self.assertEqual(Cultura.objects.get().nome, 'Soja')

    def test_create_cultura_with_invalid_produtor_rural(self):
        cultura_data = {
            "nome": "Soja",
            "produtor_rural": 9999  # Invalid produtor_rural ID
        }
        response = self.client.post('/api/cultura/', cultura_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_produtor_rural_with_empty_name(self):
        self.produtor_rural_data["nome"] = ""
        response = self.client.post('/api/produtor_rural/', self.produtor_rural_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.", response.data['nome'])

    def test_retrieve_produtor_rural_with_cultures(self):
        produtor = ProdutorRural.objects.create(**self.produtor_rural_data)
        Cultura.objects.create(nome="Soja", produtor_rural=produtor)
        Cultura.objects.create(nome="Milho", produtor_rural=produtor)
        
        response = self.client.get(f'/api/produtor_rural/{produtor.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], produtor.nome)
        self.assertEqual(len(response.data['culturas']), 2)  # Verifica se duas culturas estão associadas
        self.assertEqual(response.data['culturas'][0]['nome'], "Soja")
        self.assertEqual(response.data['culturas'][1]['nome'], "Milho")


    def test_update_produtor_rural(self):
        produtor = ProdutorRural.objects.create(**self.produtor_rural_data)
        update_data = {
            "nome": "João Atualizado",
            "nome_fazenda": "Fazenda Atualizada",
        }
        response = self.client.patch(f'/api/produtor_rural/{produtor.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        produtor.refresh_from_db()
        self.assertEqual(produtor.nome, "João Atualizado")
        self.assertEqual(produtor.nome_fazenda, "Fazenda Atualizada")

    def test_update_produtor_rural_with_valid_cultures(self):
        produtor = ProdutorRural.objects.create(**self.produtor_rural_data)
        cultura1 = Cultura.objects.create(nome="Soja", produtor_rural=produtor)
        cultura2 = Cultura.objects.create(nome="Milho", produtor_rural=produtor)
        
        update_data = {
            "nome": "João Silva Atualizado",
            "culturas": [
                {"nome": "Algodão"},
                {"nome": "Café"}
            ]
        }
        
        response = self.client.patch(f'/api/produtor_rural/{produtor.id}/', update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        produtor.refresh_from_db()
        self.assertEqual(produtor.nome, "João Silva Atualizado")
        self.assertEqual(Cultura.objects.count(), 2)  # Deve haver 2 novas culturas
        self.assertEqual(produtor.cultura_set.count(), 2)  # O produtor deve ter 2 culturas associadas
        self.assertEqual(produtor.cultura_set.first().nome, "Algodão")
        self.assertEqual(produtor.cultura_set.last().nome, "Café")

    def test_update_produtor_rural_with_invalid_culture(self):
        produtor = ProdutorRural.objects.create(**self.produtor_rural_data)
        Cultura.objects.create(nome="Soja", produtor_rural=produtor)
        
        update_data = {
            "culturas": [
                {"nome": ""}  # Nome da cultura inválido
            ]
        }
        
        response = self.client.patch(f'/api/produtor_rural/{produtor.id}/', update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is not a valid choice.", response.data['nome'][0])

    def test_delete_produtor_rural(self):
        produtor = ProdutorRural.objects.create(**self.produtor_rural_data)
        response = self.client.delete(f'/api/produtor_rural/{produtor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProdutorRural.objects.count(), 0)

