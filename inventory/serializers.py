from rest_framework import serializers
from .models import Frame, LensProduct


class FrameSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = Frame
        fields = '__all__'

    def get_product_code(self, obj):
        return obj.get_product_code()


class LensProductSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = LensProduct
        fields = '__all__'

    def get_product_code(self, obj):
        return obj.get_product_code()
