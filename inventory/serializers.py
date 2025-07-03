from rest_framework import serializers
from inventory.models import Frame, SingleVision, Bifocal, Progressive, ContactLens, BaseLensProduct

class FrameSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = Frame
        fields = '__all__'

    def get_product_code(self, obj):
        return obj.get_product_code()


class BaseLensProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseLensProduct
        fields = ['company_name', 'name', 'spherical', 'cylindrical', 'pair', 'diameter', 'created_at', 'updated_at', 'purchase_price', 'sales_price']
        abstract = True

    def validate_spherical(self, value):
        if not (-24.75 <= value <= 24.75):
            raise serializers.ValidationError("Spherical power must be between -24.75 and +24.75 diopters.")
        return value

    def validate_cylindrical(self, value):
        if not (-12.75 <= value <= 12.75):
            raise serializers.ValidationError("Cylindrical power must be between -12.75 and 12.75.")
        return value

    def validate(self, data):
        if data['purchase_price'] > data['sales_price']:
            raise serializers.ValidationError("Sales price must be greater than or equal to purchase price.")
        return data


class SingleVisionSerializer(BaseLensProductSerializer):
    class Meta:
        model = SingleVision
        fields = BaseLensProductSerializer.Meta.fields + ['material_type', 'index']

    def validate_index(self, value):
        if value <= 0:
            raise serializers.ValidationError("Refractive index must be greater than or equal to 0.")
        return value


class BifocalSerializer(SingleVisionSerializer):
    class Meta:
        model = Bifocal
        fields = SingleVisionSerializer.Meta.fields + ['axis', 'add']

    def validate(self, data):
        data = super().validate(data)
        if data.get('add') is None or data.get('add') <= 0:
            raise serializers.ValidationError("Additional power (add) must be a positive value.")
        return data

class ContactLensSerializer(BaseLensProductSerializer):
    class Meta:
        model = ContactLens
        fields = BaseLensProductSerializer.Meta.fields + ['axis', 'base_curve']


class ProgressiveSerializer(BifocalSerializer):
    class Meta:
        model = Progressive
        fields = BifocalSerializer.Meta.fields + ['side']



