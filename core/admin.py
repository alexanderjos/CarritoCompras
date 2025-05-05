from django.contrib import admin

from .models import GrupoArticulo,LineaArticulo,Articulo,Cliente,CanalCliente,Pedidos,ListaPrecios,ItemsPedidos
# Register your models here.
admin.site.register(GrupoArticulo)
admin.site.register(LineaArticulo)
admin.site.register(Articulo)
admin.site.register(Cliente)
admin.site.register(CanalCliente)
admin.site.register(Pedidos)
admin.site.register(ListaPrecios)
admin.site.register(ItemsPedidos)

