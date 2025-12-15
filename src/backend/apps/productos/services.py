from django.db import transaction
from django.utils import timezone
from .models import Producto, StockConfig, HistorialRecarga, Pedido, DetallePedido, Tienda
from apps.pagos.models import MetodoPago, EstadoPago, Pago
from apps.usuarios.models import Usuario

class StockService:
    @staticmethod
    def ajustar_stock(producto, cantidad, operacion, usuario, notas=""):
        """Ajusta el stock de un producto (aumentar/reducir) y registra historial."""
        stock_anterior = producto.stock
        
        if operacion == "aumentar":
            nuevo_stock = producto.aumentar_stock(cantidad)
            tipo = 'manual' # O podría ser 'ajuste_incremento'
        elif operacion == "reducir":
            nuevo_stock = producto.reducir_stock(cantidad)
            tipo = 'manual' # O 'ajuste_reduccion'
        else:
            raise ValueError('Operación no válida. Use "aumentar" o "reducir"')
        
        HistorialRecarga.objects.create(
            producto=producto,
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=nuevo_stock,
            tipo=tipo,
            usuario=usuario,
            notas=notas or f"Ajuste manual: {operacion}"
        )
        
        return nuevo_stock

    @staticmethod
    def get_config(producto):
        try:
            return StockConfig.objects.get(producto=producto)
        except StockConfig.DoesNotExist:
            return None

    @staticmethod
    def update_config(producto, data):
        stock_minimo = data.get("stock_minimo")
        cantidad_recarga = data.get("cantidad_recarga")
        recarga_automatica_activa = data.get("recarga_automatica_activa")
        
        config, created = StockConfig.objects.get_or_create(
            producto=producto,
            defaults={
                "stock_minimo": stock_minimo or 10,
                "cantidad_recarga": cantidad_recarga or 50,
                "recarga_automatica_activa": recarga_automatica_activa if recarga_automatica_activa is not None else True,
            }
        )
        
        if not created:
            if stock_minimo is not None:
                config.stock_minimo = stock_minimo
            if cantidad_recarga is not None:
                config.cantidad_recarga = cantidad_recarga
            if recarga_automatica_activa is not None:
                config.recarga_automatica_activa = recarga_automatica_activa
            config.save()
        
        return config, created

    @staticmethod
    def ejecutar_recarga_manual(producto, usuario, notas="Recarga manual"):
        try:
            config = StockConfig.objects.get(producto=producto)
        except StockConfig.DoesNotExist:
            raise ValueError("No hay configuración de stock para este producto.")
        
        stock_anterior = producto.stock
        
        HistorialRecarga.objects.create(
            producto=producto,
            cantidad=config.cantidad_recarga,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_anterior + config.cantidad_recarga,
            tipo='manual',
            usuario=usuario,
            notas=notas
        )
        
        producto.aumentar_stock(config.cantidad_recarga)
        return {
            "producto": producto,
            "stock_anterior": stock_anterior,
            "cantidad_agregada": config.cantidad_recarga
        }

    @staticmethod
    def get_productos_bajo_stock():
        configs = StockConfig.objects.filter(
            recarga_automatica_activa=True
        ).select_related('producto', 'producto__proveedor')
        
        return [
            config for config in configs 
            if config.necesita_recarga()
        ]

class ProductService:
    @staticmethod
    def asignar_proveedor(producto_id, proveedor_id):
        producto = Producto.objects.get(id=producto_id)
        proveedor = Usuario.objects.get(id=proveedor_id, rol="proveedor", estado=True)
        producto.proveedor = proveedor
        producto.save()
        return producto, proveedor

    @staticmethod
    def asignar_masivo(proveedor_id, producto_ids):
        proveedor = Usuario.objects.get(id=proveedor_id, rol="proveedor", estado=True)
        actualizados = []
        errores = []
        
        for pid in producto_ids:
            try:
                prod = Producto.objects.get(id=pid)
                prod.proveedor = proveedor
                prod.save()
                actualizados.append(prod)
            except Producto.DoesNotExist:
                errores.append(pid)
        
        return proveedor, actualizados, errores

class OrderService:
    @staticmethod
    def create_order(user, clean_data):
        tienda_id = clean_data["tienda_id"]
        notas = clean_data.get("notas", "")
        metodo_pago_nombre = clean_data["metodo_pago"]
        monto_pago = clean_data["monto_pago"]
        detalles_data = clean_data["detalles"]

        with transaction.atomic():
            # Validate Payment Method
            try:
                metodo_pago = MetodoPago.objects.get(nombre__iexact=metodo_pago_nombre, activo=True)
            except MetodoPago.DoesNotExist:
                raise ValueError(f"Método de pago '{metodo_pago_nombre}' no válido o inactivo")

            estado_pendiente, _ = EstadoPago.objects.get_or_create(nombre="Pendiente")

            pedido = Pedido.objects.create(
                cliente=user, tienda_id=tienda_id, notas=notas
            )

            for detalle in detalles_data:
                producto_id = detalle["producto"]
                cantidad = detalle["cantidad"]
                
                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    raise ValueError(f"Producto {producto_id} no existe")
                
                producto.reducir_stock(cantidad)
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                )

            total_pedido = pedido.calcular_total()

            if float(monto_pago) != float(total_pedido):
                 raise ValueError(f"El monto del pago ({monto_pago}) no coincide con el total del pedido ({total_pedido})")

            Pago.objects.create(
                usuario=user,
                pedido=pedido,
                monto=monto_pago,
                estado=estado_pendiente,
                metodo_pago=metodo_pago
            )
            
            return pedido

    @staticmethod
    def change_status(pedido, nuevo_estado):
        if nuevo_estado == "preparando" and not pedido.puede_cambiar_a_preparando():
            raise ValueError(f"No se puede cambiar de {pedido.estado} a preparando")
        if nuevo_estado == "en_transito" and not pedido.puede_cambiar_a_en_transito():
            raise ValueError(f"No se puede cambiar de {pedido.estado} a en_transito")
        if nuevo_estado == "entregado" and not pedido.puede_cambiar_a_entregado():
            raise ValueError(f"No se puede cambiar de {pedido.estado} a entregado")

        pedido.estado = nuevo_estado
        pedido.save()

        if nuevo_estado == "cancelado":
            for detalle in pedido.detalles.all():
                detalle.producto.aumentar_stock(detalle.cantidad)
        
        return pedido
