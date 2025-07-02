from rest_framework import serializers
from .models import Customer, Doctor, Prescription, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    pd_total = serializers.FloatField(read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
