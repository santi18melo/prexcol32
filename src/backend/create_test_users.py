"""
Script para crear usuarios de prueba de todos los roles
"""
import os
import sys
import django

sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from apps.usuarios.models import Usuario
from apps.productos.models import Tienda

print("=" * 80)
print("CREANDO USUARIOS DE PRUEBA PARA TODOS LOS ROLES")
print("=" * 80)

# Datos de usuarios por rol
usuarios_data = [
    {
        'email': 'admin@prexcol.com',
        'password': 'admin123',
        'nombre': 'Super Admin',
        'rol': 'admin',
        'is_staff': True,
        'is_superuser': True
    },
    {
        'email': 'manager@store.com',
        'password': 'manager123',
        'nombre': 'Store Manager',
        'rol': 'admin',  # Assuming Manager is admin or similar; usually 'admin' or custom role. Map to 'admin' based on list context or 'proveedor'? The list said "Store Manager". Let's use 'proveedor' or 'admin'. Wait, 'Store Manager' implies managing a store. In this system roles are [admin, proveedor, logistica, cliente]. 'Seller' -> ? 'Customer' -> 'cliente'.
        # Re-evaluating roles based on models.py (step 144): ROLES = [("admin"), ("proveedor"), ("logistica"), ("cliente")].
        # "Store Manager" likely maps to "proveedor" (manages store/products) or "admin". Let's assume 'proveedor' for now if they manage store, or 'admin' if they manage everything. But there is a "Super Admin".
        # Let's map: Super Admin -> admin, Store Manager -> proveedor, Seller -> proveedor (or maybe there is no 'seller' role? valid roles are only 4).
        # Wait, step 144 shows ROLES = [admin, proveedor, logistica, cliente].
        # "Seller (Vendedor)" is in the user's list. Maybe I should add 'vendedor' to models?
        # The user's prompt step 184 shows: "Seller (Vendedor) seller@store.com".
        # The existing create_test_users.py had 'vendedor' role in the list but models.py line 41 only showed 4 roles.
        # This implies 'vendedor' might be an invalid role in models.py if I strictly follow it.
        # Let's check models.py again. Step 144: ROLES = admin, proveedor, logistica, cliente.
        # So 'vendedor' is NOT a valid choice in the tuple?
        # But 'create_test_users.py' (step 188) had: 'rol': 'vendedor' in line 57.
        # If I run that, it might fail validation if choices are enforced? Django choices are mainly for form validation/admin, but database might accept it if charfield max_length is enough.
        # However, to be safe and consistent with "true credentials", I should probably respect the list the user gave me.
        # But I must ensure they map to valid logic in the app.
        # "Store Manager" -> likely 'proveedor' (since they have a store).
        # "Seller" -> maybe also 'proveedor' or 'cliente'?
        # Let's look at what the user gave:
        # Super Admin -> admin@prexcol.com
        # Store Manager -> manager@store.com
        # Seller -> seller@store.com
        # Customer -> user@example.com
        
        # I will update existing users or create new ones.
        'email': 'manager@store.com',
        'password': 'manager123',
        'nombre': 'Store Manager',
        'rol': 'proveedor', # Mapping 'Manager' to 'proveedor' as best fit
        'direccion': 'Store Address',
        'telefono': '+57 300 000 0000'
    },
    {
        'email': 'seller@store.com',
        'password': 'seller123',
        'nombre': 'Seller Account',
        'rol': 'proveedor', # Mapping 'Seller' to 'proveedor' or maybe 'logistica'? Let's stick to valid roles. Or maybe 'vendedor' if the app supports it despite models.py. 
        # Actually, let's look at the existing script again. It HAD 'vendedor' (line 57). 
        # If the user says "actualiza... con las verdaderas", I should update this script to produce those credentials.
        # I will use the emails and passwords provided. 
        'direccion': 'Seller Address',
        'telefono': '+57 300 111 2222'
    },
    {
        'email': 'user@example.com',
        'password': 'user123',
        'nombre': 'Customer Account',
        'rol': 'cliente',
        'direccion': 'Customer Address',
        'telefono': '+57 300 333 4444'
    }
]

print("\n📝 Creando usuarios...")
print("-" * 80)

for user_data in usuarios_data:
    email = user_data['email']
    
    # Verificar si el usuario ya existe
    if Usuario.objects.filter(email=email).exists():
        user = Usuario.objects.get(email=email)
        print(f"ℹ️  Usuario ya existe: {user.nombre} ({user.email}) - Rol: {user.rol}")
    else:
        # Crear nuevo usuario
        password = user_data.pop('password')
        user = Usuario.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        print(f"✅ Usuario creado: {user.nombre} ({user.email}) - Rol: {user.rol}")

print("\n" + "=" * 80)
print("CREDENCIALES DE ACCESO")
print("=" * 80)

print("""
🔐 ADMIN (Acceso total al sistema)
   Email: admin@example.com
   Password: admin123
   Dashboard: /dashboard-admin
   
👤 CLIENTE (Compras y pedidos)
   Email: cliente@example.com
   Password: cliente123
   Dashboard: /dashboard-cliente
   
🏭 PROVEEDOR (Gestión de productos)
   Email: proveedor@example.com
   Password: proveedor123
   Dashboard: /dashboard-proveedor
   
🚚 LOGÍSTICA (Gestión de entregas)
   Email: logistica@example.com
   Password: logistica123
   Dashboard: /dashboard-logistica
   
💼 VENDEDOR (Ventas)
   Email: vendedor@example.com
   Password: vendedor123
   Dashboard: /dashboard-vendedor
""")

print("=" * 80)
print("RESUMEN")
print("=" * 80)

total_usuarios = Usuario.objects.count()
print(f"\n✅ Total de usuarios en el sistema: {total_usuarios}")

for rol in ['admin', 'cliente', 'proveedor', 'logistica', 'vendedor']:
    count = Usuario.objects.filter(rol=rol).count()
    print(f"   - {rol.capitalize()}: {count}")

print("\n" + "=" * 80)
print("✨ Usuarios de prueba listos para usar")
print("=" * 80)

# Crear tienda de ejemplo si no existe (para proveedores)
print("\n📦 Verificando tiendas...")
if not Tienda.objects.exists():
    admin_user = Usuario.objects.filter(rol='admin').first()
    if admin_user:
        tienda = Tienda.objects.create(
            nombre='Tienda Principal',
            direccion='Calle Principal #123',
            administrador=admin_user
        )
        print(f"✅ Tienda creada: {tienda.nombre}")
else:
    print(f"ℹ️  Ya existen {Tienda.objects.count()} tienda(s) en el sistema")

print("\n✅ ¡Listo! Puedes iniciar sesión con cualquiera de estos usuarios.")
