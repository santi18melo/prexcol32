from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Factura
from .serializers import FacturaSerializer
from .permissions import IsOwnerOrAdmin
from .services import InvoiceService
from pagination import StandardResultsSetPagination

class FacturaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver y descargar facturas.
    """
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'rol', None) == 'admin':
            return Factura.objects.all()
        return Factura.objects.filter(cliente=user)

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        factura = self.get_object()
        if not factura.archivo_pdf:
            InvoiceService.trigger_pdf_generation(factura.id)
            return Response(
                {"detail": "PDF generation started. Please try again in a moment."},
                status=status.HTTP_202_ACCEPTED
            )
        
        return Response({"url": factura.archivo_pdf.url})
