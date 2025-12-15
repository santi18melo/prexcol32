from django.utils import timezone
from django.db.models import Sum
from .models import DetalleVenta

class VentaService:
    @staticmethod
    def get_reporte_diario(queryset):
        hoy = timezone.now().date()
        ventas_hoy = queryset.filter(fecha_venta__date=hoy)
        
        total_vendido = ventas_hoy.aggregate(Sum('total'))['total__sum'] or 0
        cantidad_ventas = ventas_hoy.count()
        
        return {
            'fecha': hoy,
            'total_vendido': total_vendido,
            'cantidad_ventas': cantidad_ventas,
            'ventas_queryset': ventas_hoy
        }

    @staticmethod
    def get_ventas_proveedor(user):
        if getattr(user, 'rol', None) != 'proveedor':
            raise ValueError('No eres proveedor')
            
        detalles = DetalleVenta.objects.filter(producto__proveedor=user).order_by('-venta__fecha_venta')
        total_historico = detalles.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        
        return {
            'detalles_queryset': detalles,
            'total_historico': total_historico
        }

    @staticmethod
    def create_from_payment(pago):
        from .models import Venta, DetalleVenta
        from django.db import transaction
        
        pedido = pago.pedido
        if hasattr(pedido, 'venta_registrada'):
            return None

        with transaction.atomic():
            # Crear Venta
            venta = Venta.objects.create(
                pedido=pedido,
                cliente=pedido.cliente,
                total=pedido.total,
                cantidad_items=0 
            )
            
            # Crear Detalles
            detalles_venta = []
            cantidad_total = 0
            for detalle_pedido in pedido.detalles.all():
                detalles_venta.append(DetalleVenta(
                    venta=venta,
                    producto=detalle_pedido.producto,
                    cantidad=detalle_pedido.cantidad,
                    precio_unitario=detalle_pedido.precio_unitario,
                    subtotal=detalle_pedido.subtotal
                ))
                cantidad_total += detalle_pedido.cantidad
            
            DetalleVenta.objects.bulk_create(detalles_venta)
            
            # Actualizar cantidad total real
            venta.cantidad_items = cantidad_total
            venta.save()
            return venta
