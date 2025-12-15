from django.utils import timezone
from .models import Usuario
try:
    from apps.ventas.models import Pedido, DetallePedido
except ImportError:
    Pedido = None
    DetallePedido = None
from django.db.models import Sum
from datetime import timedelta
import psutil

class AuthService:
    @staticmethod
    def login_user(user):
        """
        Updates last login and returns user.
        Token generation is typically handled by JWT library utils,
        but we can wrap it if we want strict service usage.
        For now, let's keep the core business update here.
        """
        if not user.estado:
            return None # Or raise specific exception
        
        user.ultimo_ingreso = timezone.now()
        user.save()
        return user

class AdminDashboardService:
    @staticmethod
    def get_advanced_metrics(time_range):
         # Create Date Delta
        now = timezone.now()
        start_date = now
        
        if time_range == '20s': start_date = now - timedelta(seconds=20)
        elif time_range == '1m': start_date = now - timedelta(minutes=1)
        elif time_range == '1h': start_date = now - timedelta(hours=1)
        elif time_range == '1d': start_date = now - timedelta(days=1)
        elif time_range == '1w': start_date = now - timedelta(weeks=1)
        elif time_range == '1mo': start_date = now - timedelta(days=30)
        elif time_range == '3mo': start_date = now - timedelta(days=90)
        elif time_range == '6mo': start_date = now - timedelta(days=180)
        elif time_range == '1y': start_date = now - timedelta(days=365)
        else: start_date = now - timedelta(weeks=1) # Default

        # --- SALES METRICS ---
        sales_data = {
            'total_orders': 0,
            'total_revenue': 0,
            'top_products': [],
            'bottom_products': []
        }
        
        if Pedido and DetallePedido:
            # Filter orders in range
            orders_query = Pedido.objects.filter(fecha_creacion__gte=start_date)
            sales_data['total_orders'] = orders_query.count()
            sales_data['total_revenue'] = orders_query.aggregate(Sum('total'))['total__sum'] or 0

            # Top Products
            product_stats = DetallePedido.objects.filter(pedido__fecha_creacion__gte=start_date)\
                .values('producto__nombre')\
                .annotate(qty=Sum('cantidad'))\
                .order_by('-qty')
                
            sales_data['top_products'] = list(product_stats[:5])
            sales_data['bottom_products'] = list(product_stats.order_by('qty')[:5])

        # --- USER METRICS ---
        users_data = {
            'active': Usuario.objects.filter(estado=True).count(),
            'inactive': Usuario.objects.filter(estado=False).count(),
            'new_users': Usuario.objects.filter(fecha_creacion__gte=start_date).count(),
            'top_buyers': []
        }

        # --- PLATFORM METRICS ---
        try:
            if psutil:
                cpu_p = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
            else:
                 raise ImportError("psutil not available")
        except:
            cpu_p = 0
            mem = type('obj', (object,), {'percent': 0, 'used': 0, 'total': 1})
            disk = type('obj', (object,), {'percent': 0})

        platform_data = {
            'cpu_load': cpu_p,
            'memory_usage': mem.percent,
            'memory_used_gb': round(mem.used / (1024**3), 2),
            'disk_usage': disk.percent,
            'server_time': now.strftime("%H:%M:%S")
        }

        return {
            'range': time_range,
            'sales': sales_data,
            'users': users_data,
            'platform': platform_data
        }
