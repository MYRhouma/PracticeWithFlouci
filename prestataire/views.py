from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from prestataire.models import Prestataire
from prestataire.serializers import PrestataireSerializer


# Create your views here.

class PrestataireAPIView(APIView):

    def get(self, *args, **kwargs):
        prestataires = Prestataire.objects.all()
        serializer = PrestataireSerializer(prestataires, many=True)
        return Response(serializer.data)