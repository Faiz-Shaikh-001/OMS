from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_first_name(self, value):
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value
