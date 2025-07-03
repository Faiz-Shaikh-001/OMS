from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_name(self, value):
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("Name must only contain letters.")
        return value
