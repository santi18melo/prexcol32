from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
