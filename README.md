# VMS
## Vendor Management System (VMS)


Overview
The Vendor Management System (VMS) is a Django-based web application designed to manage vendors and purchase orders. It provides functionality to create, update, retrieve, and delete vendor and purchase order records, as well as analyze vendor performance metrics.






Features
Vendor Management: Allows users to manage vendors, including creating, updating, retrieving, and deleting vendor records.
Purchase Order Management: Enables users to manage purchase orders, including creating, updating, retrieving, and deleting purchase order records.
Token-based Authentication: Utilizes token-based authentication for secure access to the API endpoints.
Vendor Performance Analysis: Provides API endpoints to analyze vendor performance metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.




### How to run the application.

Step 1:

* Clone the application to your local machine
``` 
git clone https://github.com/Yashjain18111/VMS.git
```
* Go into vms_project directory
```
cd vms_project
```
Step 2:

* Create a virtual environment:

``` 
python -m venv venv
source venv/bin/activate   # On Windows use ./venv/Scripts/activate
```
<br>
Step 3:
* Install the dependencies from the requirements file

```
pip install -r requirements.txt
```
Database Setup:

Configure your database settings in settings.py.

Run database migrations:
```
python manage.py migrate
```
Run the Development Server:
```
python manage.py runserver
```
Accessing the API:

Use API endpoints to interact with the application.

For authentication, generate a token using the generate-token/ endpoint.

API Endpoints
Vendors

List/Create Vendors:
Endpoint: /vendors/
Methods: GET, POST

Retrieve/Update/Delete Vendor:
Endpoint: /vendors/<vendor_code>/
Methods: GET, PUT, DELETE
Purchase Orders
List/Create Purchase Orders:
Endpoint: /purchase_orders/



Methods: GET, POST
Retrieve/Update/Delete Purchase Order:
Endpoint: /purchase_orders/<po_id>/

Methods: GET, PUT, DELETE
Vendor Performance Analysis
Vendor Performance Metrics:
Endpoint: /api/vendors/<vendor_id>/performance/

Method: GET
Acknowledge Purchase Order
Acknowledge Purchase Order:
Endpoint: /api/purchase_orders/<po_id>/acknowledge/
Method: POST
Generate Token
Generate Token:
Endpoint: /generate-token/
Method: POST


Technologies Used
Django: Backend web framework

Django REST Framework: Toolkit for building Web APIs

SQLite: Database system
Python: Programming language for backend development

Contributors
Yash Jain

