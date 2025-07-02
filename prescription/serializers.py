from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    pd_total = serializers.FloatField(read_only=True)
    class Meta:
        model = Prescription
        fields = '__all__'
