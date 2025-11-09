# Testing Documentation

## Test Coverage

This project includes comprehensive test coverage for all major components of the Vendor Management System.

## Test Suites

### 1. VendorModelTest
Tests for the Vendor model functionality:
- `test_vendor_creation` - Verifies vendor objects are created correctly
- `test_vendor_code_unique` - Ensures vendor_code uniqueness constraint works

### 2. PurchaseOrderModelTest
Tests for the PurchaseOrder model:
- `test_purchase_order_creation` - Verifies purchase order creation
- `test_po_number_unique` - Ensures po_number uniqueness constraint

### 3. TokenGenerationTest
Tests for authentication token generation:
- `test_generate_token_success` - Tests successful token generation
- `test_generate_token_missing_username` - Tests error handling for missing username
- `test_token_reuse` - Verifies same token is returned for existing users

### 4. VendorAPITest
Complete CRUD testing for Vendor API endpoints:
- `test_create_vendor` - POST /api/vendors/
- `test_list_vendors` - GET /api/vendors/
- `test_retrieve_vendor` - GET /api/vendors/{id}/
- `test_update_vendor` - PUT /api/vendors/{id}/
- `test_delete_vendor` - DELETE /api/vendors/{id}/
- `test_vendor_api_without_authentication` - Tests authentication requirement

### 5. PurchaseOrderAPITest
Complete CRUD testing for Purchase Order API endpoints:
- `test_create_purchase_order` - POST /api/purchase_orders/
- `test_list_purchase_orders` - GET /api/purchase_orders/
- `test_retrieve_purchase_order` - GET /api/purchase_orders/{id}/
- `test_update_purchase_order` - PUT /api/purchase_orders/{id}/
- `test_delete_purchase_order` - DELETE /api/purchase_orders/{id}/

### 6. VendorPerformanceTest
Tests for vendor performance metrics API:
- `test_get_vendor_performance` - GET /api/vendors/{id}/performance/
- `test_vendor_performance_not_found` - Tests 404 handling

### 7. VendorMetricsSignalTest
Tests for the automatic performance metrics calculation system:
- `test_on_time_delivery_rate_calculation` - Verifies on-time delivery % calculation
- `test_quality_rating_calculation` - Verifies quality rating average calculation
- `test_fulfillment_rate_calculation` - Verifies fulfillment rate calculation

### 8. AcknowledgePurchaseOrderTest
Tests for purchase order acknowledgment:
- `test_acknowledge_purchase_order_not_found` - Tests error handling for non-existent orders

## Running Tests

### Run All Tests
```bash
# Local environment
python VMS\manage.py test app

# Docker
docker-compose exec web python manage.py test app
```

### Run Specific Test Class
```bash
python VMS\manage.py test app.tests.VendorAPITest
```

### Run Specific Test Method
```bash
python VMS\manage.py test app.tests.VendorAPITest.test_create_vendor
```

### Run with Verbose Output
```bash
python VMS\manage.py test app --verbosity=2
```

## Test Database

Tests use Django's built-in test database, which is created and destroyed automatically. The test database is completely separate from your development database, so running tests won't affect your data.

## Key Testing Patterns

### 1. Authentication Setup
Most API tests use token authentication:
```python
self.user = User.objects.create_user(username='testuser', password='testpass')
self.token = Token.objects.create(user=self.user)
self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
```

### 2. Testing Signals
Signal-driven metrics are tested by creating purchase orders and verifying the vendor metrics are updated automatically:
```python
PurchaseOrder.objects.create(...)  # Creates order
self.vendor.refresh_from_db()      # Reload vendor from database
self.assertEqual(...)               # Check metrics updated
```

### 3. Testing API Responses
Standard pattern for API testing:
```python
response = self.client.post('/api/vendors/', data, format='json')
self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## Code Coverage

To generate a code coverage report:

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' VMS\manage.py test app

# Generate report
coverage report

# Generate HTML report
coverage html
```

## Continuous Integration

These tests are designed to be run in CI/CD pipelines. They:
- Use in-memory SQLite database (fast)
- Don't require external services
- Complete in ~6 seconds
- Have zero flaky tests

## Bug Fixes Made During Testing

1. **Signal Handler Bug**: Fixed incorrect string subtraction in average response time calculation
2. **Missing Import**: Added `timezone` import to views.py
3. **URL Routing**: Fixed duplicate `/api/` prefix in performance endpoint
4. **Null Handling**: Added proper null checking for quality rating average

## Future Test Improvements

Consider adding:
- Integration tests with PostgreSQL
- Performance/load tests
- Tests for edge cases in metric calculations
- Tests for concurrent purchase order updates
- API rate limiting tests (if implemented)
