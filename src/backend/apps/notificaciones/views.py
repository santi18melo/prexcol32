from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notificacion, TipoNotificacion, EstadoNotificacion
from .serializers import (
    NotificacionSerializer,
    TipoNotificacionSerializer,
    EstadoNotificacionSerializer
)
from .services import NotificationService
from pagination import StandardResultsSetPagination

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def enviar(self, request):
        """
        Endpoint simulado para enviar una notificación.
        Esperamos: { "tipo_id": 1, "mensaje": "Hola", "destino": "user@example.com" }
        """
        # Validate input existence
        required = ['tipo_id', 'mensaje', 'destino']
        if not all(k in request.data for k in required):
             return Response({"error": "Faltan datos requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            NotificationService.enviar_notificacion(request.user, request.data)
            return Response({"message": "Notificación enviada (simulada)"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        updated_notif = NotificationService.marcar_leida(notificacion)
        return Response(self.get_serializer(updated_notif).data)

    @action(detail=False, methods=['get'], url_path='historial/(?P<usuario_id>[^/.]+)')
    def historial(self, request, usuario_id=None):
        # Verificar permisos: solo admin o el mismo usuario
        if str(request.user.id) != usuario_id and not request.user.is_staff:
            return Response({"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN)
        
        notificaciones = Notificacion.objects.filter(usuario_id=usuario_id)
        page = self.paginate_queryset(notificaciones)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)

class TipoNotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoNotificacion.objects.all()
    serializer_class = TipoNotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

class EstadoNotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstadoNotificacion.objects.all()
    serializer_class = EstadoNotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
