from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from ..services import AdminDashboardService

@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_advanced_metrics(request):
    """
    Returns advanced metrics for the Admin Dashboard:
    - Sales (count, top/bottom products)
    - Users (active/inactive, stats)
    - Platform (CPU, RAM, load)
    """
    time_range = request.query_params.get('range', '1h') # 20s, 1m, 1h, 1d, 1w, 1mo, 3mo, 6mo, 1y
    
    data = AdminDashboardService.get_advanced_metrics(time_range)

    return Response(data)
