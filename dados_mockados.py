import requests
from faker import Faker
import random

# Configurações
url = "http://127.0.0.1:8000/api/produtor_rural/"
fake = Faker('pt_BR')

culturas_possiveis = [{'nome': cultura} for cultura in ['Soja', 'Milho', 'Algodão', 'Café', 'Cana de Açúcar']]

def gerar_dados_produtor():
    usa_cpf = random.choice([True, False])
    cpf_ou_cnpj = fake.cpf() if usa_cpf else fake.cnpj()
    nome = fake.name()
    nome_fazenda = fake.company()
    cidade = fake.city()
    estado = fake.state_abbr()
    area_total = round(random.uniform(100, 10000), 2)  # Área total entre 100 e 10000 hectares
    area_agricultavel = round(random.uniform(0, area_total * 0.7), 2)  # Até 70% da área total
    area_vegetacao = round(random.uniform(0, area_total - area_agricultavel), 2)  # O restante até o limite da área total
    culturas = random.sample(culturas_possiveis, k=random.randint(1, 3))  # De 1 a 3 culturas

    return {
        "cpf_cnpj": cpf_ou_cnpj,
        "usa_cpf": usa_cpf,
        "nome": nome,
        "nome_fazenda": nome_fazenda,
        "cidade": cidade,
        "estado": estado,
        "area_total_hectares": area_total,
        "area_agricultavel_hectares": area_agricultavel,
        "area_vegetacao_hectares": area_vegetacao,
        "culturas": culturas
    }

def criar_produtores_rurais(n=20):
    for _ in range(n):
        dados = gerar_dados_produtor()
        response = requests.post(url, json=dados)
        if response.status_code == 201:
            print(f"Produtor {dados['nome']} criado com sucesso.")
        else:
            print(f"Erro ao criar produtor: {response.status_code} - {response.text}")

if __name__ == "__main__":
    criar_produtores_rurais(20)
