from django.db import models
from pos_project.choices import EstadoEntidades

#Creamos un modelo
class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True)
    codigo_grupo = models.CharField(max_length=25, null=False)
    nombre_grupo = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)


    def __str__(self): 
        return self.nombre_grupo

    class Meta:
        db_table = 'grupos_articulos'
        ordering = ['codigo_grupo']
         
# Creamos el segundo modelo
class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True)
    codigo_linea = models.CharField(max_length=25, null=False)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_linea')
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    class Meta:
        db_table = 'lineas_articulos'
        ordering = ['codigo_linea']
# Creamos el cuarto modelo (Canal de Cliente)
class CanalCliente(models.Model):
    canal_id = models.CharField(max_length=3, primary_key=True)
    nombre_canal = models.CharField(max_length=100, null=False)
    class Meta:
        db_table = 'canal_cliente'
        ordering = ['nombre_canal']

# Creamos el tercer modelo (Clientes)
class Cliente(models.Model):
    cliente_id = models.UUIDField(primary_key=True)
    tipo_identificacion = models.CharField(max_length=1, null=False)
    nro_identificacion = models.CharField(max_length=11, null=False)
    nombres = models.CharField(max_length=150, null=False)
    direccion = models.CharField(max_length=150, null=False)
    correo_electronico = models.CharField(max_length=255, null=False)
    nro_movil = models.CharField(max_length=15, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    #Conectamos con canal_cliente
    canal_id = models.ForeignKey(CanalCliente, on_delete=models.RESTRICT, null=False, related_name='canal_cliente')
    class Meta:
        db_table = 'clientes'
        ordering = ['cliente_id']



#creamos el quinto modelo (Articulos)
class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True)
    codigo_articulo = models.CharField(max_length=25, null=False)
    codigo_barras = models.CharField(max_length=25, null=True)
    descripcion = models.CharField(max_length=150, null= False)
    presentacion = models.CharField(max_length=100, null=True)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_articulo',db_column='grupo_id')
    linea = models.ForeignKey(LineaArticulo, on_delete=models.RESTRICT, null=False, related_name='linea_articulo',db_column='linea_id')
    stock = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        db_table = 'articulos'
        ordering = ['codigo_articulo']

# Creamos el sexto modelo (Pedidos)
class Pedidos(models.Model):
    pedido_id = models.UUIDField(primary_key=True)
    nro_pedido = models.IntegerField(null=False)
    #fecha en formato datatime
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False, related_name='cliente_pedido')
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    class Meta:
        db_table = 'pedidos'
        ordering = ['fecha_pedido']

# Creamos el septimo modelo (Items_Pedidos)
class ItemsPedidos(models.Model):
    item_id = models.UUIDField(primary_key=True)
    pedido_id = models.ForeignKey(Pedidos, on_delete=models.RESTRICT, null=False, related_name='pedido_items')
    articulo_id = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='articulo_items')
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total_item = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    class Meta:
        db_table = 'items_pedidos'
        ordering = ['item_id']

# Creamos el octavo modelo (Lista Precios) relacion 1:1
class ListaPrecios(models.Model):
    articulo_id = models.OneToOneField(Articulo, on_delete=models.RESTRICT, primary_key=True, related_name='articulo_lista_precios')
    precio_1 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_2 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_3 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_4 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        db_table = 'lista_precios'
        ordering = ['articulo_id']
