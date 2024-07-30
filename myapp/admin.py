from django.contrib import admin
from myapp import models

# Registre seus modelos aqui
admin.site.register(models.Embalagem)
admin.site.register(models.TipoSabor)
admin.site.register(models.Sabor)
admin.site.register(models.Cobertura)
admin.site.register(models.Pedido)

# Monta Pote
class SelSaborInline(admin.TabularInline):
    model = models.SelSabor
    extra = 0

@admin.register(models.MontaPote)
class MontaPoteAdmin(admin.ModelAdmin):
    inlines = [
        SelSaborInline
    ] 

# Sacola de Itens
class MontaPoteInline(admin.TabularInline):
    model = models.SacolaItens.potes.through
    extra = 0

class PedidoInline(admin.StackedInline):
    model = models.Pedido
    extra = 0
    
@admin.register(models.SacolaItens)
class SacolaItensAdmin(admin.ModelAdmin):
    fields = ('preco',)
    readonly_fields = ('preco',)  # Adicione o campo readonly para mostrar o preço total
    inlines = [PedidoInline,MontaPoteInline]