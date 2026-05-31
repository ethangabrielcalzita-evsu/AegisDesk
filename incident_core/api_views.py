from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import AutomatedIncidentSerializer

class AutomatedIncidentIngestView(APIView):  # <-- Check spelling here!
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AutomatedIncidentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Incident logged successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)