"""
API ViewSets for VMS
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone

from app.models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, VendorPerformanceSerializer, PurchaseOrderSerializer


@api_view(['POST'])
def generate_token(request):
    """
    Generate or retrieve authentication token for a user.
    Creates user if doesn't exist.
    """
    if request.method == 'POST':
        username = request.data.get('username')
        if username:
            user, created = User.objects.get_or_create(username=username)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class VendorListCreate(generics.ListCreateAPIView):
    """
    List all vendors or create a new vendor.
    GET /api/vendors/
    POST /api/vendors/
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vendor instance.
    GET /api/vendors/{id}/
    PUT /api/vendors/{id}/
    DELETE /api/vendors/{id}/
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Get vendor by ID from URL parameter"""
        vendor_id = self.kwargs.get('vendor_id')
        return get_object_or_404(Vendor, id=vendor_id)


class VendorPerformanceAPIView(APIView):
    """
    Retrieve vendor performance metrics.
    GET /api/vendors/{vendor_id}/performance/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(
                {"message": "Vendor not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class PurchaseOrderListCreate(generics.ListCreateAPIView):
    """
    List all purchase orders or create a new purchase order.
    GET /api/purchase_orders/
    POST /api/purchase_orders/
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a purchase order instance.
    GET /api/purchase_orders/{pk}/
    PUT /api/purchase_orders/{pk}/
    DELETE /api/purchase_orders/{pk}/
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AcknowledgePurchaseOrderAPIView(APIView):
    """
    Acknowledge a purchase order by setting acknowledgment date.
    POST /api/purchase_orders/{po_id}/acknowledge/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return Response(
                {"message": "Purchase order acknowledged successfully"},
                status=status.HTTP_200_OK
            )
        except PurchaseOrder.DoesNotExist:
            return Response(
                {"message": "Purchase order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
