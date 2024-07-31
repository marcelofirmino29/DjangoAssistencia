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

    # acompanhamentos Disponiveis
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
    tamanho = models.ForeignKey(Tamanho, related_name='tamanho', on_delete=models.CASCADE, null=True)
    acompanhamentos = models.ManyToManyField(Acompanhamento)
    quantidade = models.PositiveIntegerField(null=True)
    
    def preco_total(self):
        preco_tamanho = self.tamanho.preco if self.tamanho else 0
        preco_acompanhamentos = sum(acompanhamento.preco for acompanhamento in self.acompanhamentos.all())
        preco_sabores = 0
        for selsabor in self.pizza.all():
            preco_sabor = selsabor.sabor.tipo.preco
            preco_sabores += preco_sabor
        total_pizza = preco_tamanho + preco_acompanhamentos + preco_sabores
        total = total_pizza * self.quantidade
        return total 

    def __str__(self):
        return f"ID: {self.id} / pizza: {self.tamanho.tipo} / Qtd: {self.quantidade} / {self.preco_total()}"

    class Meta:
        verbose_name = 'B - MontaPizza'
        verbose_name_plural = 'B - MontaPizza'
        
# Seleciona Sabores 
class SelSabor(models.Model):
    pizza = models.ForeignKey(MontaPizza, related_name='pizza', on_delete=models.CASCADE, null=True)
    sabor = models.ForeignKey(Sabor, related_name='sabor', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Sabor: {self.sabor.nome}, Pizza: {self.pizza}"
    
    class Meta:
        verbose_name = 'A - SelSabor'
        verbose_name_plural = 'A - SelSabor'

# Sacolas de Itens
class SacolaItens(models.Model):
    pizzas = models.ManyToManyField(MontaPizza)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Armazena o valor como um número decimal
  
    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'  # Formata o valor com 2 casas decimais

    def preco_total(self):
        # Calcule a soma dos preços de todos os pizzas na sacola
        sacola_total = 0
        for pizza in self.pizzas.all():
            sacola_total += pizza.preco_total()
        self.preco = sacola_total
        self.save()
        return sacola_total
        
    def __str__(self):
        return f"CARRINHO: {self.id} / {self.preco_total()}"

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