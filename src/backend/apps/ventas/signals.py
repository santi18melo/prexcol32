from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.pagos.models import Pago
from .services import VentaService

@receiver(post_save, sender=Pago)
def crear_venta_al_aprobar_pago(sender, instance, created, **kwargs):
    """
    Crea un registro de Venta cuando un Pago es aprobado (estado 'Aprobado' o similar).
    Delegates logic to VentaService.
    """
    if instance.estado.nombre.lower() in ['aprobado', 'completado', 'pagado']:
        VentaService.create_from_payment(instance)
