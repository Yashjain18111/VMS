"""
DEPRECATED: serializers moved to app.api.serializers
Kept for backward compatibility. Import from app.api.serializers instead.
"""
from app.api.serializers import (
    VendorSerializer,
    VendorPerformanceSerializer,
    PurchaseOrderSerializer,
)

__all__ = [
    'VendorSerializer',
    'VendorPerformanceSerializer',
    'PurchaseOrderSerializer',
]
