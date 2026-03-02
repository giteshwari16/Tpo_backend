from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import PlacementProfile
from .serializers import PlacementProfileSerializer
"""Onboarding uses only the new PlacementProfile; legacy profiles do not satisfy onboarding."""

class MePlacementProfile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            p = PlacementProfile.objects.get(user=request.user)
        except PlacementProfile.DoesNotExist:
            return Response({"detail": "not_created"}, status=status.HTTP_404_NOT_FOUND)
        return Response(PlacementProfileSerializer(p).data)

    def post(self, request):
        try:
            PlacementProfile.objects.get(user=request.user)
            return Response({"detail": "already_exists"}, status=status.HTTP_400_BAD_REQUEST)
        except PlacementProfile.DoesNotExist:
            pass
        ser = PlacementProfileSerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            obj = ser.save()
            return Response(PlacementProfileSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            p = PlacementProfile.objects.get(user=request.user)
        except PlacementProfile.DoesNotExist:
            return Response({"detail": "not_found"}, status=status.HTTP_404_NOT_FOUND)
        ser = PlacementProfileSerializer(p, data=request.data, partial=True, context={"request": request})
        if ser.is_valid():
            obj = ser.save()
            return Response(PlacementProfileSerializer(obj).data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class OnboardingStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exists = PlacementProfile.objects.filter(user=request.user).exists()
        return Response({"profile_created": exists})
