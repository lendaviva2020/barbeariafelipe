"""
Admin Users Management Views
"""

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersListView(generics.ListAPIView):
    """List all users (admin)"""
    permission_classes = (IsAdminUser,)
    
    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'created_at': user.created_at
            })
        
        return Response(data)

