"""
Signal handlers for VMS models
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, F, ExpressionWrapper, fields

from .models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, created, **kwargs):
    """
    Automatically update vendor performance metrics when a purchase order is saved.
    
    Calculates:
    - On-Time Delivery Rate: Percentage of completed orders delivered on time
    - Quality Rating Average: Average quality rating of completed orders
    - Average Response Time: Average time to acknowledge orders (in hours)
    - Fulfillment Rate: Percentage of completed orders not canceled
    """
    vendor = instance.vendor
    
    # Get all completed orders for this vendor
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    
    # Calculate On-Time Delivery Rate
    on_time_delivery_count = completed_orders.filter(
        delivery_date__lte=instance.delivery_date
    ).count()
    vendor.on_time_delivery_rate = (
        (on_time_delivery_count / completed_orders.count()) * 100
        if completed_orders.exists() else 0
    )
    
    # Calculate Quality Rating Average
    completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
    quality_avg = completed_orders_with_rating.aggregate(
        Avg('quality_rating')
    )['quality_rating__avg']
    vendor.quality_rating_avg = quality_avg if quality_avg is not None else 0.0
    
    # Calculate Average Response Time (in hours)
    acknowledged_orders = completed_orders.filter(acknowledgment_date__isnull=False)
    if acknowledged_orders.exists():
        response_times = acknowledged_orders.annotate(
            response_time=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
        ).aggregate(Avg('response_time'))['response_time__avg']
        vendor.average_response_time = (
            response_times.total_seconds() / 3600
            if response_times else 0
        )
    else:
        vendor.average_response_time = 0
    
    # Calculate Fulfillment Rate
    fulfilled_orders = completed_orders.exclude(status='canceled')
    vendor.fulfillment_rate = (
        (fulfilled_orders.count() / completed_orders.count()) * 100
        if completed_orders.exists() else 0
    )
    
    # Save vendor instance with updated performance metrics
    vendor.save()
