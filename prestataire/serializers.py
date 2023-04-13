from rest_framework.serializers import ModelSerializer

from prestataire.models import Prestataire


class PrestataireSerializer(ModelSerializer):
    class Meta:
        model = Prestataire
        fields = ['id', 'user','wallet']