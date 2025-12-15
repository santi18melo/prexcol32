from django.utils import timezone
from .models import Notificacion, TipoNotificacion, EstadoNotificacion

class NotificationService:
    @staticmethod
    def enviar_notificacion(usuario, data):
        """
        Sends (simulates) a notification.
        data: { 'tipo_id': int, 'mensaje': str, 'destino': str }
        """
        tipo_id = data.get('tipo_id')
        mensaje = data.get('mensaje')
        # destino unused in model simplified version as we create it for 'usuario'
        
        try:
           tipo = TipoNotificacion.objects.get(id=tipo_id)
        except TipoNotificacion.DoesNotExist:
            raise ValueError("Tipo de notificación no válido")
        
        # Logic to create notification
        # For now, just create object
        # In real world, send email/push here.
        
        # Simplification: create simple notification record
        # Note: 'usuario' here is the one initiating? Or receiving?
        # Assuming receiving for this context.
        return Notificacion.objects.create(
            usuario=usuario,
            tipo=tipo,
            mensaje=mensaje,
            # estado default
        )
        
    @staticmethod
    def marcar_leida(notificacion):
        if not notificacion.leida:
            notificacion.leida = True
            notificacion.fecha_lectura = timezone.now()
            notificacion.save()
        return notificacion
