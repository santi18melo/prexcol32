from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Pago, MetodoPago
from .serializers import (
    PagoSerializer, 
    TransaccionSerializer, 
    MetodoPagoSerializer, 
)
from .services import PaymentService
from pagination import StandardResultsSetPagination

class PagoViewSet(viewsets.ModelViewSet):
    serializer_class = PagoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'rol', None) in ['admin', 'comprador']:
            return Pago.objects.all()
        return Pago.objects.filter(usuario=user)

    def perform_create(self, serializer):
        # We can delegate to service here if complex, but perform_create expects to just save.
        # Minimal viable separation:
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def transaccion(self, request):
        """
        Endpoint para registrar una transacción asociada a un pago existente.
        Esperamos: { "pago_id": 1, "monto": 100.00, "referencia_externa": "XYZ", "estado": "aprobado" }
        """
        pago_id = request.data.get('pago_id')
        if not pago_id:
            return Response({"error": "pago_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        pago = get_object_or_404(Pago, id=pago_id)
        
        # Check permissions
        if pago.usuario != request.user and getattr(request.user, 'rol', None) != 'admin':
             return Response({"error": "No tiene permiso sobre este pago"}, status=status.HTTP_403_FORBIDDEN)

        # Prepare data for Service
        data = request.data.copy()
        # Remove pago_id from data if service/serializer handles it, but Transaccion needs it.
        # Service register_transaction expects 'pago' object and 'data' dict usually excluding relation if not handled
        # But here logic is simple.
        
        # Use Serializer for validation only? Or pass to Service?
        # Ideally: Controller validates input -> Service executes -> Controller returns response.
        
        # Validate input using Serializer (standard DRF practice)
        data['pago'] = pago.id
        serializer = TransaccionSerializer(data=data)
        if serializer.is_valid():
             # Delegate creation to service to keep "Creation" logic there
             # Extract validated data
             t_data = serializer.validated_data
             # remove 'pago' from validated data if it's already passed as arg, or keep it.
             # Transaccion model needs 'pago'.
             # Let's simplify: Service handles creation.
             try:
                 # Note: TransaccionSerializer.validated_data will contain 'pago' instance if using ModelSerializer
                 # So we need to be careful. usage of **validated_data might clash if we pass pago separately
                 # If we use serializer.save(), it returns the instance. 
                 # To strictly use Service:
                 transaccion = PaymentService.register_transaction(pago, {k:v for k,v in t_data.items() if k != 'pago'})
                 return Response(TransaccionSerializer(transaccion).data, status=status.HTTP_201_CREATED)
             except Exception as e:
                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def estado(self, request, pk=None):
        pago = self.get_object()
        data = PaymentService.get_payment_status(pago)
        return Response(data)

class MetodoPagoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetodoPago.objects.filter(activo=True)
    serializer_class = MetodoPagoSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
