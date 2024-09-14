from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Create your views here.

class ProtectedData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"message": "This is protected data."}
        return Response(data)



class CachedData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_role = request.user.role
        cache_key = f"user_{request.user.id}_role_{user_role}"

        # Check for cache-busting conditions (e.g., user role, URL params, etc.)
        if 'bust_cache' in request.GET:
            cache.delete(cache_key)

        # Cache data per user/role combination
        data = cache.get(cache_key)
        if not data:
            data = {"message": f"This is data for role: {user_role}"}
            cache.set(cache_key, data, 60 * 15)  # Cache for 15 minutes

        return Response(data)
