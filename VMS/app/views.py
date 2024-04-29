from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Vendor,PurchaseOrder
from .serializers import VendorSerializer,PurchaseOrderSerializer,VendorPerformanceSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Count
from rest_framework.decorators import api_view


@api_view(['POST'])
def generate_token(request):
    if request.method == 'POST':
        # Extract username from the request data
        username = request.data.get('username')
        if username:
            # Get or create the user object
            user, created = User.objects.get_or_create(username=username)
            # Get or create the token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Username is required'}, status=400)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
from django.shortcuts import get_object_or_404

class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    print(serializer_class)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self):
        vendor_code = self.kwargs.get('vendor_code')
        print(vendor_code)
        return get_object_or_404(Vendor, id=vendor_code)
    
    
class PurchaseOrderListCreate(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
class VendorPerformanceRetrieve(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

  


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, created, **kwargs):
    vendor = instance.vendor
    
    # Calculate On-Time Delivery Rate
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivery_count = completed_orders.filter(delivery_date__lte=instance.delivery_date).count()
    vendor.on_time_delivery_rate = (on_time_delivery_count / completed_orders.count()) * 100 if completed_orders.exists() else 0
    
    # Calculate Quality Rating Average
    completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
    vendor.quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']
    
    # Calculate Average Response Time
    acknowledged_orders = completed_orders.filter(acknowledgment_date__isnull=False)
    vendor.average_response_time = acknowledged_orders.aggregate(Avg('acknowledgment_date' - 'issue_date'))['acknowledgment_date__avg']
    
    # Calculate Fulfillment Rate
    fulfilled_orders = completed_orders.exclude(status='canceled')
    vendor.fulfillment_rate = (fulfilled_orders.count() / completed_orders.count()) * 100 if completed_orders.exists() else 0
    
    # Save vendor instance with updated performance metrics
    vendor.save()


class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()  # Assuming timezone is imported
            purchase_order.save()
            return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"message": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)


