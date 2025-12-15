from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Venta
from .serializers import VentaSerializer
from apps.usuarios.permissions import IsAdmin
from pagination import StandardResultsSetPagination
from .services import VentaService

class VentaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar ventas. Solo lectura.
    Acceso restringido a administradores.
    """
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_venta__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_venta__lte=fecha_fin)
            
        return queryset

    @action(detail=False, methods=['get'])
    def reporte_diario(self, request):
        """Reporte de ventas del día actual"""
        data = VentaService.get_reporte_diario(self.get_queryset())
        
        # Pagination
        page = self.paginate_queryset(data['ventas_queryset'])
        if page is not None:
             serializer = self.get_serializer(page, many=True)
             response = self.get_paginated_response(serializer.data)
             response.data['meta']['summary'] = {
                 'total_vendido': data['total_vendido'],
                 'cantidad_ventas': data['cantidad_ventas'],
                 'fecha': data['fecha']
             }
             return response
        
        return Response({
            'fecha': data['fecha'],
            'total_vendido': data['total_vendido'],
            'cantidad_ventas': data['cantidad_ventas'],
            'ventas': VentaSerializer(data['ventas_queryset'], many=True).data
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mis_ventas_proveedor(self, request):
        """
        Retorna los detalles de venta de productos que pertenecen al proveedor actual.
        """
        try:
            result = VentaService.get_ventas_proveedor(request.user)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
            
        detalles = result['detalles_queryset']
        total_historico = result['total_historico']
        
        page = self.paginate_queryset(detalles)
        
        def format_detalle(d):
            return {
                'id': d.id,
                'fecha': d.venta.fecha_venta,
                'producto': d.producto.nombre,
                'cantidad': d.cantidad,
                'precio_unitario': d.precio_unitario,
                'subtotal': d.subtotal,
                'cliente': d.venta.cliente.nombre
            }

        if page is not None:
             data = [format_detalle(d) for d in page]
             response = self.get_paginated_response(data)
             response.data['meta']['total_historico_vendido'] = total_historico
             return response

        data = [format_detalle(d) for d in detalles]    
        return Response({
            'total_historico': total_historico,
            'ventas': data
        })
