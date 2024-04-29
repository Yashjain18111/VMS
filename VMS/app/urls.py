# urls.py
from django.urls import path
from .views import VendorListCreate,generate_token,AcknowledgePurchaseOrderAPIView, VendorPerformanceAPIView, VendorRetrieveUpdateDestroy,PurchaseOrderListCreate, PurchaseOrderRetrieveUpdateDestroy

urlpatterns = [
    path('vendors/', VendorListCreate.as_view(), name='vendor-list-create'),
    path('vendors/<str:vendor_code>/', VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    path('purchase_orders/', PurchaseOrderListCreate.as_view(), name='purchase_order_list_create'),
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchase_order_retrieve_update_destroy'),
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('generate-token/', generate_token, name='generate_token'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge_purchase_order'),
]




