# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Django REST Framework-based Vendor Management System (VMS) that tracks vendor performance metrics including on-time delivery, quality ratings, response times, and fulfillment rates. Uses token-based authentication for API access.

## Common Commands

### Docker (Recommended)
```bash
# Build and start container
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop container
docker-compose down

# Execute Django commands in container
docker-compose exec web python manage.py <command>

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test
```

### Local Environment Setup
```powershell
# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirement.txt
```

### Database Operations
```powershell
# Apply migrations
python VMS\manage.py migrate

# Create migrations after model changes
python VMS\manage.py makemigrations

# Create superuser for admin access
python VMS\manage.py createsuperuser
```

### Development Server
```powershell
# Run development server
python VMS\manage.py runserver

# Run on specific port
python VMS\manage.py runserver 8080
```

### Django Shell
```powershell
# Open Django shell for testing/debugging
python VMS\manage.py shell
```

### Testing
```powershell
# Run all tests
python VMS\manage.py test

# Run tests for specific app
python VMS\manage.py test app

# Run specific test case
python VMS\manage.py test app.tests.TestClassName
```

## Architecture

### Project Structure
- **VMS/VMS/** - Django project configuration (settings, urls, wsgi, asgi)
- **VMS/app/** - Main application containing all business logic
- **db.sqlite3** - SQLite database (development)
- **.venv/** - Python virtual environment

### Core Models

**Vendor** - Central entity storing vendor information and performance metrics
- Unique `vendor_code` identifier
- Performance fields: `on_time_delivery_rate`, `quality_rating_avg`, `average_response_time`, `fulfillment_rate`
- These metrics are automatically calculated and updated via signals

**PurchaseOrder** - Tracks orders placed with vendors
- Links to Vendor via ForeignKey
- Uses `po_number` as unique identifier
- Stores `items` as JSONField
- Tracks order lifecycle: `order_date`, `issue_date`, `delivery_date`, `acknowledgment_date`
- Optional `quality_rating` field (affects vendor metrics)

**HistoricalPerformance** - Snapshots of vendor performance over time
- ForeignKey to Vendor
- Stores same performance metrics as Vendor model at specific dates

### Authentication & Authorization
- Token-based authentication using DRF's TokenAuthentication
- All API endpoints (except token generation) require authentication
- Token generation endpoint: `POST /api/generate-token/` with `username` in request body
- Include token in requests: `Authorization: Token <token_key>`

### Signal-Driven Metrics
The `post_save` signal on PurchaseOrder automatically recalculates vendor performance metrics:
- **On-Time Delivery Rate**: Percentage of completed orders delivered by delivery_date
- **Quality Rating Average**: Mean of quality_rating for completed orders with ratings
- **Average Response Time**: Mean time between issue_date and acknowledgment_date
- **Fulfillment Rate**: Percentage of completed orders not canceled

### API Endpoints Pattern
Base URL: `/api/`

**Vendors:**
- `GET/POST /api/vendors/` - List/create vendors
- `GET/PUT/DELETE /api/vendors/<vendor_code>/` - Retrieve/update/destroy vendor by ID (note: uses `id` not `vendor_code` despite URL pattern)
- `GET /api/vendors/<vendor_id>/performance/` - Get vendor performance metrics

**Purchase Orders:**
- `GET/POST /api/purchase_orders/` - List/create orders
- `GET/PUT/DELETE /api/purchase_orders/<pk>/` - Retrieve/update/destroy order
- `POST /api/purchase_orders/<po_id>/acknowledge/` - Acknowledge order (sets acknowledgment_date)

### Development Notes

**Settings Configuration:**
- Django 4.1.1+ (currently using Django 5.0.4)
- DEBUG=True (development mode - change for production)
- SQLite database (suitable for development)
- SECRET_KEY is exposed (must be changed for production)
- REST_FRAMEWORK configured for TokenAuthentication

**Key Implementation Details:**
- Views use DRF's generic class-based views (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
- Serializers expose all model fields (`fields = '__all__'`)
- VendorPerformanceSerializer only exposes performance-related fields
- `VendorRetrieveUpdateDestroy.get_object()` uses `id` from kwargs despite URL param being named `vendor_code`
- Signal handler in views.py recalculates all vendor metrics on every PurchaseOrder save
- Missing `timezone` import in `AcknowledgePurchaseOrderAPIView` (line 113 references undefined `timezone`)

**Testing Approach:**
- Test infrastructure is in place but no tests are currently implemented
- Use Django's TestCase framework for writing tests
- Run tests with `python VMS\manage.py test`
