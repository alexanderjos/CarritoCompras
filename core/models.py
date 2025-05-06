from django.db import models
from pos_project.choices import EstadoEntidades, EstadoOrden
import uuid
# IMPORTAMOS USUARIO de accounts
from accounts.models import Usuario
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
#Creamos el modelo tipo de identificacion
class TipoIdentificacion(models.Model):
    tipo_id = models.CharField(max_length=1, primary_key=True)
    nombre_tipo = models.CharField(max_length=50, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    class Meta:
        db_table = 'tipo_identificacion'
        ordering = ['tipo_id']
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
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, null=False, related_name='tipo_identificacion_cliente')
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

# Crear el modelo de vendedor
class Vendedor(models.Model):
    vendedor_id = models.UUIDField(primary_key=True)
    nombres = models.CharField(max_length=150, null=False)
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, null=False, related_name='tipo_identificacion_vendedor')
    nro_identificacion = models.CharField(max_length=11, null=False)
    correo_electronico = models.CharField(max_length=255, null=False)
    nro_movil = models.CharField(max_length=15, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    class Meta:
        db_table = 'vendedores'
        ordering = ['vendedor_id']


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



class OrdenCompraCliente(models.Model):
    pedido_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nro_pedido = models.BigAutoField(unique=True,null=False,auto_created=True)
    fecha_pedido = models.DateField(auto_now_add=True, null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.RESTRICT, null=False)
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.IntegerField(choices=EstadoOrden.choices, default=EstadoOrden.PENDIENTE)
    notas = models.TextField(null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False)

    def actualizar_total(self):
        """Actualiza el total de la orden basado en los items"""
        total = sum(item.total_item for item in self.item_orden_compra.all())
        self.importe = total
        self.save()
    def __call__(self, *args, **kwds):
        return f"Orden #{self.nro_pedido} - {self.cliente}"
    class Meta:
        db_table = 'ordenes_compra_cliente'
        ordering = ['fecha_creacion']
class ItemOrdenCompraCliente(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(OrdenCompraCliente, on_delete=models.CASCADE, null=False, related_name='items_orden_compra')
    nro_item = models.PositiveIntegerField(default=1, null=False)
    articulo = models.ForeignKey('Articulo', on_delete=models.RESTRICT, null=False, related_name='articulo_item_orden_compra')
    cantidad = models.PositiveIntegerField(null=False, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    total_item = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    estado = models.IntegerField(choices=EstadoEntidades,default=EstadoEntidades.ACTIVO)
    creado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT,null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False)

    def save(self, *args, **kwargs):
        # Calcular el total del item
        self.total_item = self.cantidad * self.precio_unitario

        # Si no se ha establecido el precio unitario, tomarlo del artículo
        if self.precio_unitario == 0:
            try:
                lista_precio = self.articulo.listaprecio
                self.precio_unitario = lista_precio.precio_1
                self.total_item = self.cantidad * self.precio_unitario
            except:
                pass
                super().save(*args, **kwargs)
                # Actualizar el total de la orden
                self.pedido.actualizar_total()

    def __str__(self):
        return f"{self.cantidad} x {self.articulo.descripcion}"

    class Meta:
        db_table = "items_ordenes_compra_cliente"

       







