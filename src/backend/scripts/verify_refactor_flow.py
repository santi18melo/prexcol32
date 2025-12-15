import os
import sys
import django
from decimal import Decimal

# Setup Django Environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from apps.usuarios.models import Usuario
from apps.productos.models import Producto, Tienda, Categoria, StockConfig
from apps.pagos.models import MetodoPago, EstadoPago
from apps.productos.services import OrderService, ProductService, StockService
from apps.pagos.services import PaymentService
from apps.ventas.services import VentaService

def run_test():
    print("--- INICIANDO TEST DE INTEGRACIÓN (FLUJO COMPLETO) ---")

    # 1. SETUP DATOS
    print("\n1. Creando Datos de Prueba...")
    # Usuario Proveedor
    proveedor, _ = Usuario.objects.get_or_create(
        email="prov_test@test.com", 
        defaults={"username": "prov_test", "rol": "proveedor", "estado": True, "password": "pass"}
    )
    # Usuario Cliente
    cliente, _ = Usuario.objects.get_or_create(
        email="cli_test@test.com", 
        defaults={"username": "cli_test", "rol": "cliente", "estado": True, "password": "pass"}
    )
    # Tienda
    tienda, _ = Tienda.objects.get_or_create(
        nombre="Tienda Test", 
        defaults={"direccion": "Calle Falsa 123", "administrador": proveedor} # Simplification: admin usually manages
    )
    # Categoria (Fix for ForeignKey)
    from apps.categorias.models import Categoria
    categoria, _ = Categoria.objects.get_or_create(nombre="General", defaults={"activa": True})

    # Producto
    producto, created = Producto.objects.get_or_create(
        nombre="Producto Test Flow",
        tienda=tienda,
        defaults={
            "descripcion": "Desc", 
            "precio": Decimal("100.00"), 
            "stock": 50, 
            "proveedor": proveedor,
            "categoria": categoria  # Add required field
        }
    )
    if not created:
        producto.stock = 50
        producto.save()
    
    # Metodo Pago
    metodo, _ = MetodoPago.objects.get_or_create(nombre="Tarjeta", defaults={"activo": True})
    
    print(f"   Producto: {producto.nombre} (Stock: {producto.stock})")
    print(f"   Cliente: {cliente.nombre}")

    # 2. CREAR PEDIDO (OrderService)
    print("\n2. Probando OrderService.create_order...")
    order_data = {
        "tienda_id": tienda.id,
        "metodo_pago": metodo.nombre,
        "monto_pago": 200.00, # 2 units * 100
        "detalles": [
            {"producto": producto.id, "cantidad": 2} # Buy 2
        ]
    }
    
    try:
        pedido = OrderService.create_order(cliente, order_data)
        print(f"   Pedido ID: {pedido.id} creado con estado: {pedido.estado}")
        print(f"   Total Pedido: {pedido.total}")
        
        # Validar Stock reducido
        producto.refresh_from_db()
        print(f"   Nuevo Stock Producto: {producto.stock} (Esperado: 48)")
        assert producto.stock == 48
    except Exception as e:
        print(f"   ERROR en crear_pedido: {e}")
        return

    # 3. PROCESAR PAGO (PaymentService & Venta Automatic Trigger)
    print("\n3. Probando Venta Automática (Simulando Aprobación de Pago)...")
    # El pedido crea el pago en estado pendiente. Lo buscamos.
    pago = pedido.pago_set.first()
    print(f"   Pago encontrado: {pago.id} - Estado: {pago.estado.nombre}")
    
    # Simular cambio de estado a Aprobado
    estado_aprobado, _ = EstadoPago.objects.get_or_create(nombre="Aprobado")
    pago.estado = estado_aprobado
    pago.save() # Esto dispara el Signal -> VentaService.create_from_payment
    
    # Validar Venta creada
    pedido.refresh_from_db()
    if hasattr(pedido, 'venta_registrada'):
        venta = pedido.venta_registrada
        print(f"   ÉXITO: Venta creada automáticamente. ID: {venta.id}")
        print(f"   Total Venta: {venta.total}")
        print(f"   Items Venta: {venta.cantidad_items}")
    else:
        print("   FALLO: No se creó la venta automáticamente.")
    
    print("\n--- TEST FINALIZADO CORRECTAMENTE ---")

if __name__ == "__main__":
    run_test()
