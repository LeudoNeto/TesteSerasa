from django.db import models

class ProdutorRural(models.Model):
    cpf_cnpj = models.CharField(max_length=18, unique=True, help_text='CPF ou CNPJ do produtor', blank=True)
    usa_cpf = models.BooleanField(default=True, help_text='Se o produtor usa CPF (True) ou CNPJ (False)')
    nome = models.CharField(max_length=100, help_text='Nome do produtor')
    nome_fazenda = models.CharField(max_length=100, help_text='Nome da fazenda')
    cidade = models.CharField(max_length=100, help_text='Cidade onde a fazenda está localizada')
    estado = models.CharField(max_length=2, help_text='Estado onde a fazenda está localizada')
    area_total_hectares = models.DecimalField(max_digits=10, decimal_places=2, help_text='Área total da fazenda em hectares')
    area_agricultavel_hectares = models.DecimalField(max_digits=10, decimal_places=2, help_text='Área agricultável em hectares')
    area_vegetacao_hectares = models.DecimalField(max_digits=10, decimal_places=2, help_text='Área de vegetação em hectares')

    def __str__(self):
        return f'{self.nome} - {self.nome_fazenda}'

class Cultura(models.Model):
    nome = models.CharField(max_length=50, choices=[
        ('Soja', 'Soja'),
        ('Milho', 'Milho'),
        ('Algodão', 'Algodão'),
        ('Café', 'Café'),
        ('Cana de Açúcar', 'Cana de Açúcar'),
    ], help_text='Nome da cultura')
    produtor_rural = models.ForeignKey(ProdutorRural, on_delete=models.CASCADE, help_text='Produtor rural que cultiva essa cultura')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'produtor_rural'], name='unique_cultura_per_produtor')
        ]

    def __str__(self):
        return self.nome
