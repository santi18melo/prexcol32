from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Tienda, Producto, Pedido, DetallePedido, Seccion, StockConfig
from .serializers import (
    TiendaSerializer,
    ProductoSerializer,
    ProductoListSerializer,
    PedidoSerializer,
    PedidoCreateSerializer,
    PedidoUpdateEstadoSerializer,
    PedidoListSerializer,
    DetallePedidoSerializer,
    SeccionSerializer,
)
from .permissions import (
    IsAdmin,
    IsCliente,
    IsProveedor,
    IsLogistica,
    IsProductoOwnerOrAdmin,
)
from .services import StockService, ProductService, OrderService
from pagination import StandardResultsSetPagination


# ======================== TIENDA VIEWSET ========================

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.filter(activa=True)
    serializer_class = TiendaSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve", "mis_tiendas"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def mis_tiendas(self, request):
        tiendas = Tienda.objects.filter(administrador=request.user)
        page = self.paginate_queryset(tiendas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tiendas, many=True)
        return Response(serializer.data)


# ======================== PRODUCTO VIEWSET ========================

class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Producto.objects.filter(activo=True)
        
        rol = getattr(self.request.user, "rol", None)
        if rol in ["admin"] or self.request.user.is_superuser:
            return Producto.objects.filter(activo=True)
        if rol == "proveedor":
            return Producto.objects.filter(proveedor=self.request.user, activo=True)
        # Cliente or others
        return Producto.objects.filter(activo=True)

    def get_serializer_class(self):
        if self.action == "list":
            return ProductoListSerializer
        return ProductoSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = []  # Public access
        elif self.action in ["por_tienda"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["create", "destroy"]:
            permission_classes = [IsAdmin]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsProductoOwnerOrAdmin]
        elif self.action in ["ajustar_stock", "historial_recargas", "config_stock"]:
            permission_classes = [IsAdmin | IsProveedor]
        elif self.action == "mis_productos":
            permission_classes = [IsProveedor]
        elif self.action in ["ejecutar_recarga", "productos_stock_bajo", "asignar_proveedor", "asignar_productos_masivo"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def por_tienda(self, request):
        tienda_id = request.query_params.get("tienda_id")
        if not tienda_id:
            return Response({"error": "Parámetro tienda_id requerido"}, status=status.HTTP_400_BAD_REQUEST)
        productos = self.get_queryset().filter(tienda_id=tienda_id)
        page = self.paginate_queryset(productos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsProveedor])
    def mis_productos(self, request):
        productos = Producto.objects.filter(proveedor=request.user, activo=True)
        page = self.paginate_queryset(productos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin | IsProveedor])
    def ajustar_stock(self, request, pk=None):
        producto = self.get_object()
        try:
            cantidad = request.data.get("cantidad")
            if cantidad is None:
                raise ValueError("Parámetro cantidad requerido")
            
            try:
                cantidad = int(cantidad)
            except ValueError:
                raise ValueError("Cantidad debe ser un número entero")

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que 0")

            nuevo_stock = StockService.ajustar_stock(
                producto, 
                cantidad, 
                request.data.get("operacion", "aumentar"), 
                request.user
            )
            return Response({
                "mensaje": "Stock actualizado correctamente",
                "nuevo_stock": nuevo_stock,
                "producto_id": producto.id
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def asignar_proveedor(self, request, pk=None):
        try:
            prod, prov = ProductService.asignar_proveedor(pk, request.data.get("proveedor_id"))
            return Response({
                "mensaje": f"Producto '{prod.nombre}' asignado a '{prov.nombre}'",
                "producto_id": prod.id,
                "proveedor_id": prov.id,
                "proveedor_nombre": prov.nombre,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get", "post", "patch"], permission_classes=[IsAdmin | IsProveedor])
    def config_stock(self, request, pk=None):
        producto = self.get_object()
        
        if request.method == "GET":
            config = StockService.get_config(producto)
            if not config:
                return Response({
                    "mensaje": "No hay configuración de stock para este producto",
                    "producto_id": producto.id,
                    "stock_actual": producto.stock,
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "producto_id": producto.id,
                "producto_nombre": producto.nombre,
                "stock_actual": producto.stock,
                "stock_minimo": config.stock_minimo,
                "cantidad_recarga": config.cantidad_recarga,
                "recarga_automatica_activa": config.recarga_automatica_activa,
                "ultima_recarga": config.ultima_recarga,
                "total_recargas": config.total_recargas,
            })
        
        # POST/PATCH
        config, created = StockService.update_config(producto, request.data)
        return Response({
            "mensaje": "Configuración de stock actualizada" if not created else "Configuración de stock creada",
            "producto_id": producto.id,
            "stock_minimo": config.stock_minimo,
            "cantidad_recarga": config.cantidad_recarga,
            "recarga_automatica_activa": config.recarga_automatica_activa,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def ejecutar_recarga(self, request, pk=None):
        producto = self.get_object()
        try:
            result = StockService.ejecutar_recarga_manual(
                producto, 
                request.user, 
                request.data.get('notas', 'Recarga manual desde admin')
            )
            return Response({
                "mensaje": f"Stock recargado exitosamente",
                "producto": result['producto'].nombre,
                "stock_anterior": result['stock_anterior'],
                "stock_nuevo": result['producto'].stock,
                "cantidad_agregada": result['cantidad_agregada'],
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[IsAdmin])
    def productos_stock_bajo(self, request):
        configs = StockService.get_productos_bajo_stock()
        
        data = [{
            "id": c.producto.id,
            "nombre": c.producto.nombre,
            "stock_actual": c.producto.stock,
            "stock_minimo": c.stock_minimo,
            "cantidad_recarga": c.cantidad_recarga,
            "proveedor": c.producto.proveedor.nombre if c.producto.proveedor else None,
        } for c in configs]
        
        # Manually pagination for list
        page = self.paginate_queryset(data)
        if page is not None:
             return self.get_paginated_response(page)

        return Response({
            "total": len(data),
            "productos": data,
        })

    @action(detail=True, methods=["get"], permission_classes=[IsAdmin | IsProveedor])
    def historial_recargas(self, request, pk=None):
        producto = self.get_object()
        # Direct query for simplicity, or move to Service if complex logic needed
        historial = producto.historial_recargas.all().order_by('-fecha_creacion')
        page = self.paginate_queryset(historial)
        
        def format_hist(h):
            return {
                "id": h.id,
                "cantidad": h.cantidad,
                "stock_anterior": h.stock_anterior,
                "stock_nuevo": h.stock_nuevo,
                "tipo": h.tipo,
                "usuario": h.usuario.nombre if h.usuario else "Sistema",
                "notas": h.notas,
                "fecha": h.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            }

        if page is not None:
            data = [format_hist(h) for h in page]
            return self.get_paginated_response(data)

        data = [format_hist(h) for h in historial[:20]] # Fallback limit
        return Response({
            "producto": producto.nombre,
            "total_recargas": historial.count(),
            "historial": data,
        })

    @action(detail=False, methods=["post"], permission_classes=[IsAdmin])
    def asignar_productos_masivo(self, request):
        proveedor_id = request.data.get("proveedor_id")
        producto_ids = request.data.get("producto_ids", [])
        
        if not proveedor_id:
            return Response({"error": "Se requiere proveedor_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not producto_ids or not isinstance(producto_ids, list):
             return Response({"error": "Se requiere una lista de producto_ids"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            prov, actualizados, errores = ProductService.asignar_masivo(proveedor_id, producto_ids)
            return Response({
                "mensaje": f"{len(actualizados)} productos asignados a {prov.nombre}",
                "proveedor": {"id": prov.id, "nombre": prov.nombre},
                "productos_actualizados": [{"id": p.id, "nombre": p.nombre} for p in actualizados],
                "errores": errores if errores else None,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ======================== PEDIDO VIEWSET ========================

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        rol = getattr(self.request.user, "rol", None)
        if rol in ["admin"] or self.request.user.is_superuser:
            return Pedido.objects.all()
        if rol == "cliente":
            return Pedido.objects.filter(cliente=self.request.user)
        if rol == "logistica":
            return Pedido.objects.filter(estado__in=["pendiente", "preparando", "en_transito", "entregado"])
        return Pedido.objects.none()

    def get_serializer_class(self):
        if self.action == "list":
            return PedidoListSerializer
        if self.action == "crear_pedido":
            return PedidoCreateSerializer
        if self.action == "cambiar_estado":
            return PedidoUpdateEstadoSerializer
        return PedidoSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "mis_pedidos", "pendientes", "en_preparacion"]:
            permission_classes = [IsAuthenticated]
        elif self.action == "crear_pedido":
            permission_classes = [IsCliente]
        elif self.action == "cambiar_estado":
            permission_classes = [IsAdmin | IsLogistica]
        elif self.action == "destroy":
            permission_classes = [IsAdmin]
        elif self.action == "pdf_factura":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "Use el endpoint /crear_pedido/ para crear pedidos"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=False, methods=["post"], permission_classes=[IsCliente])
    def crear_pedido(self, request):
        serializer = PedidoCreateSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            pedido = OrderService.create_order(request.user, serializer.validated_data)
            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post", "put", "patch"], permission_classes=[IsAdmin | IsLogistica])
    def cambiar_estado(self, request, pk=None):
        pedido = self.get_object()
        serializer = PedidoUpdateEstadoSerializer(data=request.data, context={"request": request, "pedido": pedido})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            pedido = OrderService.change_status(pedido, serializer.validated_data["estado"])
            return Response({
                "mensaje": f"Pedido actualizado a estado: {pedido.estado}",
                "pedido": PedidoSerializer(pedido).data,
            })
        except ValueError as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[IsCliente])
    def mis_pedidos(self, request):
        pedidos = Pedido.objects.filter(cliente=request.user).order_by("-fecha_creacion")
        page = self.paginate_queryset(pedidos)
        if page is not None:
             serializer = PedidoListSerializer(page, many=True)
             return self.get_paginated_response(serializer.data)
        serializer = PedidoListSerializer(pedidos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsLogistica])
    def pendientes(self, request):
        pedidos = Pedido.objects.filter(estado="pendiente").order_by("fecha_creacion")
        page = self.paginate_queryset(pedidos)
        if page is not None:
             serializer = PedidoListSerializer(page, many=True)
             return self.get_paginated_response(serializer.data)
        serializer = PedidoListSerializer(pedidos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsLogistica])
    def en_preparacion(self, request):
        pedidos = Pedido.objects.filter(estado="preparando").order_by("fecha_creacion")
        page = self.paginate_queryset(pedidos)
        if page is not None:
             serializer = PedidoListSerializer(page, many=True)
             return self.get_paginated_response(serializer.data)
        serializer = PedidoListSerializer(pedidos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsLogistica])
    def panel_logistica(self, request):
        """
        Endpoint consolidad para el panel de logística.
        Retorna TODOS los pedidos relevantes para el flujo logístico:
        Pendientes, Preparando, En Tránsito y Entregados (Historial).
        """
        pedidos = Pedido.objects.filter(
            estado__in=["pendiente", "preparando", "en_transito", "entregado"]
        ).order_by("-fecha_creacion")
        
        page = self.paginate_queryset(pedidos)
        if page is not None:
             serializer = PedidoListSerializer(page, many=True)
             return self.get_paginated_response(serializer.data)
        serializer = PedidoListSerializer(pedidos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny], authentication_classes=[])
    def pdf_factura(self, request, pk=None):
        """
        Genera/Renderiza la factura en HTML simple para visualización/impresión.
        """
        from apps.ventas.models import Venta
        pedido = get_object_or_404(Pedido, pk=pk)
        
        # Intentar obtener la venta asociada
        try:
            venta = Venta.objects.get(pedido=pedido)
            folio = f"F-{venta.id:06d}"
            fecha = venta.fecha_venta.strftime("%d/%m/%Y %H:%M")
        except Venta.DoesNotExist:
            return HttpResponse("Factura no encontrada.", status=404)

        rows_html = ""
        for detalle in pedido.detalles.all():
            rows_html += f"""
                    <tr>
                        <td style="border-bottom: 1px solid #eee; padding: 12px; font-size: 14px;">{detalle.producto.nombre}</td>
                        <td style="border-bottom: 1px solid #eee; padding: 12px; font-size: 14px; text-align: right;">{detalle.cantidad}</td>
                        <td style="border-bottom: 1px solid #eee; padding: 12px; font-size: 14px; text-align: right;">${detalle.precio_unitario}</td>
                        <td style="border-bottom: 1px solid #eee; padding: 12px; font-size: 14px; text-align: right;">${detalle.subtotal}</td>
                    </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Factura {folio}</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #555; line-height: 1.6; margin: 0; padding: 0; background-color: #f5f5f5; }}
                .invoice-box {{ max-width: 800px; margin: 40px auto; padding: 40px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); background-color: #fff; border-radius: 8px; }}
                .header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .header-title h1 {{ margin: 0; font-size: 32px; color: #333; text-transform: uppercase; letter-spacing: 2px; }}
                .header-title p {{ margin: 5px 0 0; color: #777; font-size: 14px; }}
                .header-meta {{ text-align: right; }}
                .header-meta p {{ margin: 5px 0; font-size: 14px; color: #555; }}
                .client-section {{ background-color: #f9f9f9; padding: 25px; border-radius: 6px; margin-bottom: 40px; display: flex; justify-content: space-between; }}
                .client-col h3 {{ margin-top: 0; font-size: 14px; text-transform: uppercase; color: #888; letter-spacing: 1px; margin-bottom: 10px; }}
                .client-col p {{ margin: 3px 0; font-size: 15px; color: #333; font-weight: 500; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
                th {{ background-color: #333; color: #fff; text-align: left; padding: 12px; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }}
                th.text-right {{ text-align: right; }}
                .total-section {{ display: flex; justify-content: flex-end; align-items: center; margin-top: 20px; padding-top: 20px; border-top: 2px solid #333; }}
                .total-label {{ font-size: 16px; color: #777; margin-right: 20px; font-weight: bold; text-transform: uppercase; }}
                .total-value {{ font-size: 28px; font-weight: bold; color: #333; }}
                .footer {{ margin-top: 60px; text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #eee; padding-top: 20px; }}
                @media print {{
                    body {{ background-color: #fff; -webkit-print-color-adjust: exact; }}
                    .invoice-box {{ box-shadow: none; border: none; margin: 0; padding: 0; max-width: 100%; }}
                    .client-section {{ background-color: #f9f9f9 !important; -webkit-print-color-adjust: exact; }}
                    th {{ background-color: #333 !important; color: #fff !important; -webkit-print-color-adjust: exact; }}
                }}
            </style>
        </head>
        <body>
            <div class="invoice-box">
                <div class="header">
                    <div class="header-title">
                        <h1>Factura {folio}</h1>
                        <p style="margin-bottom: 5px; font-weight: bold;">Prex Col</p>
                        <p style="margin: 0; font-size: 12px; color: #666;">Email: prexcoloficial@gmail.com</p>
                        <p style="margin: 0; font-size: 12px; color: #666;">Tel: +57 324 664 8181</p>
                    </div>
                    <div class="header-meta">
                        <p><strong>NIT:</strong> 900.123.456-7</p>
                        <p><strong>Fecha:</strong> {fecha}</p>
                        <p><strong>Estado:</strong> {pedido.estado.upper()}</p>
                    </div>
                </div>
                
                <div class="client-section">
                    <div class="client-col">
                        <h3>Facturado A</h3>
                        <p>{pedido.cliente.nombre}</p>
                        <p style="font-size: 13px; color: #666;">{pedido.cliente.email}</p>
                    </div>
                    <div class="client-col" style="text-align: right;">
                        <h3>Tienda</h3>
                        <p>{pedido.tienda.nombre}</p>
                    </div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th class="text-right">Cant.</th>
                            <th class="text-right">Precio Unit.</th>
                            <th class="text-right">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
                
                <div class="total-section">
                    <span class="total-label">Total a Pagar</span>
                    <span class="total-value">${pedido.total}</span>
                </div>
                
                <div class="footer">
                    <p>Gracias por su compra.</p>
                    <p>Este documento es una representación impresa de un comprobante digital emitido por Prex Col.</p>
                </div>
            </div>
            
            <script>
                // Auto print after short delay to ensure rendering
                setTimeout(() => window.print(), 500);
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(html_content, content_type="text/html; charset=utf-8")

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def generar_factura(self, request, pk=None):
        from apps.ventas.models import Venta
        pedido = self.get_object()
        
        if pedido.estado != 'entregado' and not request.user.is_superuser:
            return Response(
                {"error": "Solo se pueden generar facturas de pedidos entregados"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar si ya existe venta/factura
        venta, created = Venta.objects.get_or_create(
            pedido=pedido,
            defaults={
                'cliente': pedido.cliente,
                'total': pedido.total,
                # 'cantidad_items': pedido.detalles.count() # Si el modelo lo requiere
            }
        )
        
        # Generar folio virtual basado en ID de venta
        folio = f"F-{venta.id:06d}"
        pdf_path = f"/api/productos/pedidos/{pedido.id}/pdf_factura/"
        pdf_url = request.build_absolute_uri(pdf_path)
        
        return Response({
            "mensaje": "Factura generada exitosamente",
            "numero_factura": folio,
            "archivo_pdf": pdf_url,
            "fecha_emision": venta.fecha_venta
        })

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def ver_factura(self, request, pk=None):
        """
        Retorna la info de la factura si existe
        """
        from apps.ventas.models import Venta
        pedido = self.get_object()
        try:
            venta = Venta.objects.get(pedido=pedido)
            folio = f"F-{venta.id:06d}"
            pdf_path = f"/api/productos/pedidos/{pedido.id}/pdf_factura/"
            pdf_url = request.build_absolute_uri(pdf_path)
            return Response({
                "numero_factura": folio,
                "archivo_pdf": pdf_url,
                "fecha_emision": venta.fecha_venta
            })
        except Venta.DoesNotExist:
            return Response({"error": "Factura no generada"}, status=status.HTTP_404_NOT_FOUND)


# ======================== DETALLE PEDIDO VIEWSET ========================

class DetallePedidoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DetallePedidoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        rol = getattr(self.request.user, "rol", None)
        if rol in ["admin"] or self.request.user.is_superuser:
            return DetallePedido.objects.all()
        if rol == "cliente":
            return DetallePedido.objects.filter(pedido__cliente=self.request.user)
        if rol == "logistica":
            return DetallePedido.objects.all()
        return DetallePedido.objects.none()

    @action(detail=False, methods=["get"])
    def por_pedido(self, request):
        pedido_id = request.query_params.get("pedido_id")
        if not pedido_id:
            return Response({"error": "Parámetro pedido_id requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            # Permission check - could be moved to a permission class/service but ok here for now
            if not (
                request.user.is_superuser
                or getattr(request.user, "rol", None) == "admin"
                or pedido.cliente == request.user
                or getattr(request.user, "rol", None) == "logistica"
            ):
                return Response({"error": "No tiene permiso para ver este pedido"}, status=status.HTTP_403_FORBIDDEN)
            
            detalles = DetallePedido.objects.filter(pedido_id=pedido_id)
            page = self.paginate_queryset(detalles)
            if page is not None:
                 serializer = self.get_serializer(page, many=True)
                 return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(detalles, many=True)
            return Response(serializer.data)
        except Pedido.DoesNotExist:
            return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)


# ======================== SECCION VIEWSET ========================

class SeccionViewSet(viewsets.ModelViewSet):
    queryset = Seccion.objects.filter(activa=True)
    serializer_class = SeccionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = []
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def agregar_productos(self, request, pk=None):
        seccion = self.get_object()
        producto_ids = request.data.get("producto_ids", [])
        
        if not producto_ids:
            return Response({"error": "Se requiere una lista de producto_ids"}, status=status.HTTP_400_BAD_REQUEST)
        
        productos = Producto.objects.filter(id__in=producto_ids, activo=True)
        seccion.productos.add(*productos)
        
        return Response({
            "mensaje": f"{productos.count()} productos agregados a la sección",
            "seccion": SeccionSerializer(seccion).data
        })

class ProductoSubirImagenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if "imagen" not in request.FILES:
            return Response({"error": "Se requiere una imagen"}, status=status.HTTP_400_BAD_REQUEST)

        # Logic could be in Service, but it's simple file handling
        producto.imagen = request.FILES["imagen"]
        producto.save()

        return Response({
            "mensaje": "Imagen subida correctamente",
            "imagen_url": request.build_absolute_uri(producto.imagen.url),
        })
