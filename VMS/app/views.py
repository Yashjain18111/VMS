"""
DEPRECATED: This file is kept for backward compatibility.
All views have been moved to app.api.viewsets
"""

# Import from new location for backward compatibility
from app.api.viewsets import (
    generate_token,
    VendorListCreate,
    VendorRetrieveUpdateDestroy,
    VendorPerformanceAPIView,
    PurchaseOrderListCreate,
    PurchaseOrderRetrieveUpdateDestroy,
    AcknowledgePurchaseOrderAPIView,
)

__all__ = [
    'generate_token',
    'VendorListCreate',
    'VendorRetrieveUpdateDestroy',
    'VendorPerformanceAPIView',
    'PurchaseOrderListCreate',
    'PurchaseOrderRetrieveUpdateDestroy',
    'AcknowledgePurchaseOrderAPIView',
]

