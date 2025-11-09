"""
URL Configuration for VMS API
"""
from django.urls import path
from .viewsets import (
    VendorListCreate,
    VendorRetrieveUpdateDestroy,
    VendorPerformanceAPIView,
    PurchaseOrderListCreate,
    PurchaseOrderRetrieveUpdateDestroy,
    AcknowledgePurchaseOrderAPIView,
    generate_token,
)

app_name = 'api'

urlpatterns = [
    # Authentication
    path('generate-token/', generate_token, name='generate_token'),
    
    # Vendor endpoints
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    
    # Purchase Order endpoints
    path('purchase_orders/', PurchaseOrderListCreate.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchase-order-detail'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='purchase-order-acknowledge'),
]
