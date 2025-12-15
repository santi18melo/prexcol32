from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ..serializers import UsuarioSerializer
from pagination import StandardResultsSetPagination

User = get_user_model()

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar usuarios: listar, crear, actualizar, eliminar.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """
        Retorna o actualiza los datos del usuario autenticado
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            # 'me' returns a single object, no pagination needed/possible
            return Response(serializer.data)
        
        # Para PUT y PATCH
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def proveedores(self, request):
        """
        Retorna lista de proveedores activos (solo para admin)
        """
        if not (request.user.is_superuser or getattr(request.user, 'rol', None) == 'admin'):
            return Response(
                {"error": "No tiene permisos para ver esta información"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        proveedores = User.objects.filter(rol='proveedor', estado=True)
        
        # Apply pagination
        page = self.paginate_queryset(proveedores)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)
