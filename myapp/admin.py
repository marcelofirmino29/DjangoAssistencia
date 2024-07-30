from django.contrib import admin
from myapp import models

# Registre seus modelos aqui
admin.site.register(models.Tamanho)
admin.site.register(models.TipoSabor)
admin.site.register(models.Sabor)
admin.site.register(models.Acompanhamento)
admin.site.register(models.Pedido)

# Monta pizza
class SelSaborInline(admin.TabularInline):
    model = models.SelSabor
    extra = 0

@admin.register(models.MontaPizza)
class MontaPizzaAdmin(admin.ModelAdmin):
    inlines = [
        SelSaborInline
    ] 

# Sacola de Itens
class MontaPizzaInline(admin.TabularInline):
    model = models.SacolaItens.pizzas.through
    extra = 0

class PedidoInline(admin.StackedInline):
    model = models.Pedido
    extra = 0
    
@admin.register(models.SacolaItens)
class SacolaItensAdmin(admin.ModelAdmin):
    fields = ('preco',)
    readonly_fields = ('preco',)  # Adicione o campo readonly para mostrar o preço total
    inlines = [PedidoInline,MontaPizzaInline]