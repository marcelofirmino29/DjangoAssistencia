from django.db import models
from django.contrib.auth.models import User

# Tipo de Pizza
class Tamanho(models.Model):
    tipo = models.CharField(max_length=50)
    quantidade_fatias = models.PositiveIntegerField()
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}' # Formata por ex R$ 23,30
    
    def __str__(self):
        return f'{self.tipo} | PREÇO: R$ {self.preco:.2f}'

    class Meta:
        verbose_name = '1 - Tamanho'
        verbose_name_plural = '1 - Tamanho'
    
    # Tradicional / Premium / Sorbet / Açai
class TipoSabor(models.Model):
    tipo = models.CharField(max_length=100)
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'
    
    def __str__(self):
        return f'{self.tipo} | PREÇO: R$ {self.preco:.2f}'

    class Meta:
        verbose_name = '2 - TipoSabor'
        verbose_name_plural = '2 - TipoSabor'

    # Lista de Sabores
class Sabor(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.ForeignKey(TipoSabor, 
                             related_name='tipo_sabor', 
                             on_delete=models.CASCADE)
    ativo = models.BooleanField() 
    
    def __str__(self):
        return f'{self.nome} | PREÇO: R$ {self.tipo.preco:.2f}'

    class Meta:
        verbose_name = '3 - Sabor'
        verbose_name_plural = '3 - Sabor'

    # Acompanhamentos Disponiveis
class Acompanhamento(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'
    
    def __str__(self):
        return f'{self.nome} | PREÇO: R$ {self.preco:.2f}'
    
    class Meta:
        verbose_name = '4 - Acompanhamento'
        verbose_name_plural = '4 - Acompanhamento' 

# Monta a pizza  
class MontaPizza(models.Model):
    Tamanho = models.ForeignKey(Tamanho, related_name='Tamanho', on_delete=models.CASCADE, null=True)
    Acompanhamentos = models.ManyToManyField(Acompanhamento)
    quantidade = models.PositiveIntegerField(null=True)
    
    def preco_total(self):
        preco_Tamanho = self.Tamanho.preco if self.Tamanho else 0
        preco_Acompanhamentos = sum(Acompanhamento.preco for Acompanhamento in self.Acompanhamentos.all())
        preco_sabores = 0
        for selsabor in self.pizza.all():
            preco_sabor = selsabor.sabor.tipo.preco
            quantidade_fatias = selsabor.quantidade_fatias
            preco_sabores += preco_sabor * quantidade_fatias
        total_pizza = preco_Tamanho + preco_Acompanhamentos + preco_sabores
        total = total_pizza * self.quantidade
        return total 

    def __str__(self):
        return f"ID: {self.id} / pizza: {self.Tamanho.tipo} / Qtd: {self.quantidade} / {self.preco_total()}"

    class Meta:
        verbose_name = 'B - MontaPizza'
        verbose_name_plural = 'B - MontaPizza'
        
# Seleciona Sabores 
class SelSabor(models.Model):
    pizza = models.ForeignKey(MontaPizza, related_name='pizza', on_delete=models.CASCADE, null=True)
    sabor = models.ForeignKey(Sabor, related_name='sabor', on_delete=models.CASCADE, null=True)
    quantidade_fatias = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Sabor: {self.sabor.nome}, Quantidade de Bolas: {self.quantidade_fatias}"
    
    class Meta:
        verbose_name = 'A - SelSabor'
        verbose_name_plural = 'A - SelSabor'

# Sacolas de Itens
# Sacolas de Itens
class SacolaItens(models.Model):
    pizzas = models.ManyToManyField(MontaPizza)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'

    def preco_total(self):
        # Certifica-se de que a sacola já tenha um ID antes de tentar calcular o preço total
        if not self.pk:
            return 0
        sacola_total = sum(pizza.preco_total() for pizza in self.pizzas.all())
        return sacola_total

    def save(self, *args, **kwargs):
        # Atualizar o preço antes de salvar
        self.preco = self.preco_total()
        super().save(*args, **kwargs)  # Chama o método save() real

    def __str__(self):
        return f"CARRINHO: {self.id} / {self.preco_formatado()}"

    class Meta:
        verbose_name = 'C - SacolaItens'
        verbose_name_plural = 'C - SacolaItens'


    
    # Registro do Pedido
class Pedido(models.Model):
    data_pedido = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, related_name='pedido_user', 
                             on_delete=models.PROTECT)
    itens_da_sacola = models.OneToOneField(SacolaItens, 
                                           on_delete=models.CASCADE, 
                                           null=True)    
    status = models.BooleanField()
    pago = models.BooleanField()
    # Endereço
    # Pagamento com Card / Dinheiro / Pix
    
    def __str__(self):
        return f"Pedido: {self.id} / {self.user} / (PAGO: {self.pago})"

    class Meta:
        verbose_name = 'D - Pedido'
        verbose_name_plural = 'D - Pedido'