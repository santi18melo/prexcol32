from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.usuarios.models import Usuario
from apps.productos.models import Producto, Tienda
from apps.pagos.models import MetodoPago, EstadoPago
from apps.productos.services import OrderService
from apps.categorias.models import Categoria

class Command(BaseCommand):
    help = 'Verifica el flujo completo de Pedido -> Pago -> Venta'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("--- INICIANDO TEST DE INTEGRACIÓN (FLUJO COMPLETO) ---"))

        # 1. SETUP DATOS
        self.stdout.write("1. Creando Datos de Prueba...")
        proveedor, _ = Usuario.objects.get_or_create(
            email="prov_test@test.com", 
            defaults={"nombre": "prov_test", "rol": "proveedor", "estado": True, "password": "pass"}
        )
        if not proveedor.check_password("pass"): proveedor.set_password("pass"); proveedor.save()

        cliente, _ = Usuario.objects.get_or_create(
            email="cli_test@test.com", 
            defaults={"nombre": "cli_test", "rol": "cliente", "estado": True, "password": "pass"}
        )
        if not cliente.check_password("pass"): cliente.set_password("pass"); cliente.save()

        tienda, _ = Tienda.objects.get_or_create(
            nombre="Tienda Test", 
            defaults={"direccion": "Calle Falsa 123", "administrador": proveedor}
        )
        
        categoria, _ = Categoria.objects.get_or_create(nombre="General", defaults={"activa": True})

        producto, created = Producto.objects.get_or_create(
            nombre="Producto Test Flow",
            tienda=tienda,
            defaults={
                "descripcion": "Desc", 
                "precio": Decimal("100.00"), 
                "stock": 50, 
                "proveedor": proveedor,
                "categoria": categoria
            }
        )
        if not created:
            producto.stock = 50
            producto.save()
        
        metodo, _ = MetodoPago.objects.get_or_create(nombre="Tarjeta", defaults={"activo": True})
        
        self.stdout.write(f"   Producto: {producto.nombre} (Stock: {producto.stock})")

        # 2. CREAR PEDIDO
        self.stdout.write("2. Probando OrderService.create_order...")
        order_data = {
            "tienda_id": tienda.id,
            "metodo_pago": metodo.nombre,
            "monto_pago": 200.00,
            "detalles": [
                {"producto": producto.id, "cantidad": 2}
            ]
        }
        
        try:
            pedido = OrderService.create_order(cliente, order_data)
            self.stdout.write(f"   Pedido ID: {pedido.id} creado con estado: {pedido.estado}")
            
            producto.refresh_from_db()
            if producto.stock != 48:
                 self.stdout.write(self.style.ERROR(f"   ERROR: Stock no se redujo correctamente. Actual: {producto.stock}"))
                 return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ERROR en crear_pedido: {e}"))
            return

        # 3. PROCESAR PAGO
        self.stdout.write("3. Probando Venta Automática...")
        pago = pedido.pago_set.first()
        
        # Simular Aprobación
        estado_aprobado, _ = EstadoPago.objects.get_or_create(nombre="Aprobado")
        pago.estado = estado_aprobado
        pago.save() 
        
        # Validar Venta
        pedido.refresh_from_db()
        if hasattr(pedido, 'venta_registrada'):
            venta = pedido.venta_registrada
            self.stdout.write(self.style.SUCCESS(f"   ÉXITO: Venta creada. ID: {venta.id} - Total: {venta.total}"))
        else:
            self.stdout.write(self.style.ERROR("   FALLO: No se creó la venta automáticamente."))
