"""
Serializers for VMS API
"""
from rest_framework import serializers
from app.models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Vendor model with all fields"""
    
    class Meta:
        model = Vendor
        fields = '__all__'


class VendorPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for Vendor performance metrics only"""
    
    class Meta:
        model = Vendor
        fields = [
            'id',
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate'
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseOrder model with all fields"""
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
