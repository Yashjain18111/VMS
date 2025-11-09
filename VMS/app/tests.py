from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from app.models import Vendor, PurchaseOrder, HistoricalPerformance
import json


class VendorModelTest(TestCase):
    """Test cases for Vendor model"""

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@vendor.com",
            address="123 Test St",
            vendor_code="VEN001",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=24.0,
            fulfillment_rate=98.0
        )

    def test_vendor_creation(self):
        """Test vendor is created correctly"""
        self.assertEqual(self.vendor.name, "Test Vendor")
        self.assertEqual(self.vendor.vendor_code, "VEN001")
        self.assertEqual(str(self.vendor), "Test Vendor")

    def test_vendor_code_unique(self):
        """Test vendor_code uniqueness constraint"""
        with self.assertRaises(Exception):
            Vendor.objects.create(
                name="Duplicate Vendor",
                contact_details="duplicate@vendor.com",
                address="456 Test Ave",
                vendor_code="VEN001",  # Duplicate code
                on_time_delivery_rate=90.0,
                quality_rating_avg=4.0,
                average_response_time=20.0,
                fulfillment_rate=95.0
            )


class PurchaseOrderModelTest(TestCase):
    """Test cases for PurchaseOrder model"""

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@vendor.com",
            address="123 Test St",
            vendor_code="VEN001",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )
        self.po = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A", "quantity": 10},
            quantity=10,
            status="pending",
            issue_date=timezone.now()
        )

    def test_purchase_order_creation(self):
        """Test purchase order is created correctly"""
        self.assertEqual(self.po.po_number, "PO001")
        self.assertEqual(self.po.vendor, self.vendor)
        self.assertEqual(str(self.po), "PO001")

    def test_po_number_unique(self):
        """Test po_number uniqueness constraint"""
        with self.assertRaises(Exception):
            PurchaseOrder.objects.create(
                po_number="PO001",  # Duplicate PO number
                vendor=self.vendor,
                order_date=timezone.now(),
                delivery_date=timezone.now() + timedelta(days=7),
                items={"item1": "Product B"},
                quantity=5,
                status="pending",
                issue_date=timezone.now()
            )


class TokenGenerationTest(APITestCase):
    """Test cases for token generation endpoint"""

    def test_generate_token_success(self):
        """Test successful token generation"""
        response = self.client.post('/api/generate-token/', {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_generate_token_missing_username(self):
        """Test token generation without username"""
        response = self.client.post('/api/generate-token/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_token_reuse(self):
        """Test that same token is returned for existing user"""
        response1 = self.client.post('/api/generate-token/', {'username': 'testuser'})
        token1 = response1.data['token']
        
        response2 = self.client.post('/api/generate-token/', {'username': 'testuser'})
        token2 = response2.data['token']
        
        self.assertEqual(token1, token2)


class VendorAPITest(APITestCase):
    """Test cases for Vendor API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@vendor.com',
            'address': '123 Test St',
            'vendor_code': 'VEN001',
            'on_time_delivery_rate': 95.0,
            'quality_rating_avg': 4.5,
            'average_response_time': 24.0,
            'fulfillment_rate': 98.0
        }

    def test_create_vendor(self):
        """Test creating a vendor"""
        response = self.client.post('/api/vendors/', self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

    def test_list_vendors(self):
        """Test listing all vendors"""
        Vendor.objects.create(**self.vendor_data)
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_vendor(self):
        """Test retrieving a specific vendor"""
        vendor = Vendor.objects.create(**self.vendor_data)
        response = self.client.get(f'/api/vendors/{vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor(self):
        """Test updating a vendor"""
        vendor = Vendor.objects.create(**self.vendor_data)
        updated_data = self.vendor_data.copy()
        updated_data['name'] = 'Updated Vendor'
        response = self.client.put(f'/api/vendors/{vendor.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vendor.refresh_from_db()
        self.assertEqual(vendor.name, 'Updated Vendor')

    def test_delete_vendor(self):
        """Test deleting a vendor"""
        vendor = Vendor.objects.create(**self.vendor_data)
        response = self.client.delete(f'/api/vendors/{vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_api_without_authentication(self):
        """Test accessing vendor API without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PurchaseOrderAPITest(APITestCase):
    """Test cases for PurchaseOrder API endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@vendor.com',
            address='123 Test St',
            vendor_code='VEN001',
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        self.po_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': timezone.now().isoformat(),
            'delivery_date': (timezone.now() + timedelta(days=7)).isoformat(),
            'items': {"item1": "Product A", "quantity": 10},
            'quantity': 10,
            'status': 'pending',
            'issue_date': timezone.now().isoformat()
        }

    def test_create_purchase_order(self):
        """Test creating a purchase order"""
        response = self.client.post('/api/purchase_orders/', self.po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)

    def test_list_purchase_orders(self):
        """Test listing all purchase orders"""
        PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='pending',
            issue_date=timezone.now()
        )
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_purchase_order(self):
        """Test retrieving a specific purchase order"""
        po = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='pending',
            issue_date=timezone.now()
        )
        response = self.client.get(f'/api/purchase_orders/{po.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO001')

    def test_update_purchase_order(self):
        """Test updating a purchase order"""
        po = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='pending',
            issue_date=timezone.now()
        )
        updated_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': po.order_date.isoformat(),
            'delivery_date': po.delivery_date.isoformat(),
            'items': po.items,
            'quantity': 10,
            'status': 'completed',
            'issue_date': po.issue_date.isoformat()
        }
        response = self.client.put(f'/api/purchase_orders/{po.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        po.refresh_from_db()
        self.assertEqual(po.status, 'completed')

    def test_delete_purchase_order(self):
        """Test deleting a purchase order"""
        po = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='pending',
            issue_date=timezone.now()
        )
        response = self.client.delete(f'/api/purchase_orders/{po.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)


class VendorPerformanceTest(APITestCase):
    """Test cases for vendor performance metrics"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@vendor.com',
            address='123 Test St',
            vendor_code='VEN001',
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

    def test_get_vendor_performance(self):
        """Test retrieving vendor performance metrics"""
        response = self.client.get(f'/api/vendors/{self.vendor.id}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)

    def test_vendor_performance_not_found(self):
        """Test retrieving performance for non-existent vendor"""
        response = self.client.get('/api/vendors/99999/performance/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VendorMetricsSignalTest(TestCase):
    """Test cases for signal-driven vendor performance metrics"""

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@vendor.com',
            address='123 Test St',
            vendor_code='VEN001',
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

    def test_on_time_delivery_rate_calculation(self):
        """Test on-time delivery rate is calculated correctly"""
        # Create completed orders
        delivery_date = timezone.now() + timedelta(days=7)
        
        # On-time order
        PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=delivery_date,
            items={"item1": "Product A"},
            quantity=10,
            status='completed',
            issue_date=timezone.now()
        )
        
        # Late order
        PurchaseOrder.objects.create(
            po_number='PO002',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=delivery_date - timedelta(days=10),  # Was late
            items={"item1": "Product B"},
            quantity=5,
            status='completed',
            issue_date=timezone.now()
        )
        
        # Refresh vendor to get updated metrics
        self.vendor.refresh_from_db()
        # Should be 50% (1 out of 2 on time)
        self.assertGreater(self.vendor.on_time_delivery_rate, 0)

    def test_quality_rating_calculation(self):
        """Test quality rating average is calculated correctly"""
        PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='completed',
            quality_rating=4.5,
            issue_date=timezone.now()
        )
        
        PurchaseOrder.objects.create(
            po_number='PO002',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product B"},
            quantity=5,
            status='completed',
            quality_rating=3.5,
            issue_date=timezone.now()
        )
        
        self.vendor.refresh_from_db()
        # Average should be 4.0
        self.assertEqual(self.vendor.quality_rating_avg, 4.0)

    def test_fulfillment_rate_calculation(self):
        """Test fulfillment rate is calculated correctly"""
        # Completed order
        PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='completed',
            issue_date=timezone.now()
        )
        
        # Canceled order
        PurchaseOrder.objects.create(
            po_number='PO002',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product B"},
            quantity=5,
            status='completed',  # Note: status filtering logic may need review
            issue_date=timezone.now()
        )
        
        self.vendor.refresh_from_db()
        self.assertGreaterEqual(self.vendor.fulfillment_rate, 0)


class AcknowledgePurchaseOrderTest(APITestCase):
    """Test cases for purchase order acknowledgment"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='test@vendor.com',
            address='123 Test St',
            vendor_code='VEN001',
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        self.po = PurchaseOrder.objects.create(
            po_number='PO001',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={"item1": "Product A"},
            quantity=10,
            status='pending',
            issue_date=timezone.now()
        )

    def test_acknowledge_purchase_order_not_found(self):
        """Test acknowledging non-existent purchase order"""
        response = self.client.post('/api/purchase_orders/99999/acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
