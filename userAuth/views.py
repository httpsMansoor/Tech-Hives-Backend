# views.py (create this if you don't have one)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,  # ✅ use the field directly
        "is_staff": user.is_staff,
        "is_active": user.is_active,
    })
