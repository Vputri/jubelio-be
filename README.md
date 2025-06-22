# Supermarket Data Analysis System

This Django application transforms Excel supermarket data into PostgreSQL tables and provides REST API endpoints for data visualization.

## Features

- **Data Import**: Transforms Excel dataset to PostgreSQL tables
- **Database Models**: Category, SubCategory, Product, Sales, and InventoryMovement
- **REST APIs**: Three endpoints for data visualization
- **Admin Interface**: Django admin for data management
- **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration
- **API Documentation**: Swagger/OpenAPI documentation

## Database Schema

### Models Created

1. **Category**: Product categories (e.g., Office Supplies, Furniture, Technology)
2. **SubCategory**: Sub-categories within each category
3. **Product**: Individual products with manufacturer information
4. **Sales**: Sales transactions with customer, location, and financial data
5. **InventoryMovement**: Tracks inventory movements (IN/OUT) for each product

## API Endpoints

### 1. Most Sold Products (Pie Chart)
- **Endpoint**: `GET /supermarket/api/most-sold-products/`
- **Purpose**: Returns data for pie chart showing most to least sold products
- **Response Format**:
```json
{
  "success": true,
  "data": {
    "labels": ["Product1", "Product2", ...],
    "data": [100, 95, ...],
    "total_sales": 5000
  }
}
```

### 2. Discount vs Quantity Correlation (Scatter Plot Facet)
- **Endpoint**: `GET /supermarket/api/discount-quantity-correlation/`
- **Purpose**: Returns correlation data between discount (y) and quantity (x) by state
- **Response Format**:
```json
{
  "success": true,
  "data": {
    "states": ["CA", "NY", ...],
    "correlations": [
      {
        "state": "CA",
        "avg_discount": 0.15,
        "avg_quantity": 3.2,
        "total_records": 150,
        "points": [{"x": 2, "y": 0.1}, ...]
      }
    ]
  }
}
```

### 3. Quantity by Country (Heatmap)
- **Endpoint**: `GET /supermarket/api/quantity-by-country/`
- **Purpose**: Returns quantity sold by country and category for heatmap visualization
- **Response Format**:
```json
{
  "success": true,
  "data": {
    "countries": ["United States", "Canada", ...],
    "categories": ["Office Supplies", "Furniture", ...],
    "data": [
      {
        "country": "United States",
        "category": "Office Supplies",
        "quantity": 1500
      }
    ],
    "matrix": {...}
  }
}
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- PostgreSQL (via Docker)

### Installation

1. **Clone and setup the project**:
```bash
# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Start PostgreSQL database**:
```bash
docker-compose up -d
```

3. **Run database migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Import Excel data**:
```bash
python manage.py import_excel_data kaggle_supermarket_dataset.xlsx
```

5. **Create superuser (optional)**:
```bash
python manage.py createsuperuser
```

6. **Start Django development server**:
```bash
python manage.py runserver
```

## Usage

### Access Admin Interface
- URL: http://localhost:8000/admin/
- Username: admin
- Password: (set during superuser creation)

### Test API Endpoints
```bash
# Test all endpoints
python test_api.py

# Or test individually with curl
curl http://localhost:8000/supermarket/api/most-sold-products/
curl http://localhost:8000/supermarket/api/discount-quantity-correlation/
curl http://localhost:8000/supermarket/api/quantity-by-country/
```

### API Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **Redoc**: http://localhost:8000/redoc/

## CORS Testing

### What is CORS?
Cross-Origin Resource Sharing (CORS) allows web applications to make requests to APIs hosted on different domains. This is essential for frontend applications that need to communicate with your Django backend.

### Testing CORS Functionality

1. **Start your Django server**:
```bash
python manage.py runserver
```

2. **Open the CORS test file**:
   - Open `test_cors.html` in your web browser
   - Or serve it with a simple HTTP server:
   ```bash
   python -m http.server 8080
   # Then visit http://localhost:8080/test_cors.html
   ```

3. **Test the APIs**:
   - Click the "Test API" buttons for each endpoint
   - Verify that requests succeed without CORS errors
   - Check the response data in the browser

### Expected Results
- ✅ **Success**: Green boxes with API response data
- ❌ **CORS Error**: Red boxes with error messages
- ❌ **Network Error**: Red boxes indicating server connection issues

### CORS Configuration
The application is configured with:
- `CORS_ALLOW_ALL_ORIGINS = True` (development only)
- `CORS_ALLOW_CREDENTIALS = True`
- Proper middleware placement for security

### For Production
Update `settings.py` to restrict allowed origins:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React development
    "https://yourdomain.com",  # Production domain
]
```

### Data Import Worker
The system includes a Django management command that:
- Reads the Excel file using pandas
- Cleans and transforms data (currency, discounts, dates)
- Creates database records with proper relationships
- Generates inventory movements for sales transactions

```bash
# Re-import data (clears existing data first)
python manage.py import_excel_data kaggle_supermarket_dataset.xlsx
```

## Data Processing Features

### Data Cleaning
- **Currency Values**: Removes $ symbols and converts to Decimal
- **Discounts**: Converts percentages to decimal format (0-1 range)
- **Dates**: Converts to proper date format
- **Duplicates**: Handles duplicate orders with get_or_create

### Performance Optimizations
- Uses Django ORM with select_related for efficient queries
- Implements database transactions for data integrity
- Optimized queries with proper annotations and aggregations

## File Structure
```
jubelio/
├── supermarket/
│   ├── models.py              # Database models
│   ├── views.py               # API endpoints
│   ├── admin.py               # Admin interface
│   ├── urls.py                # URL routing
│   └── management/
│       └── commands/
│           └── import_excel_data.py  # Data import worker
├── jubelio/
│   ├── settings.py            # Django settings
│   └── urls.py                # Main URL configuration
├── bin/
│   └── preview_excel.py       # Excel data preview script
├── docker-compose.yml         # PostgreSQL container
├── kaggle_supermarket_dataset.xlsx  # Source data
├── test_api.py               # API testing script
├── test_cors.html            # CORS testing interface
└── README.md                 # This file
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Ensure PostgreSQL container is running: `docker-compose ps`
   - Check database credentials in settings.py

2. **Import Errors**:
   - Verify Excel file path and format
   - Check file permissions
   - Ensure all required packages are installed

3. **API Errors**:
   - Check Django server is running
   - Verify URL patterns in urls.py
   - Check database has data imported

4. **CORS Errors**:
   - Ensure `django-cors-headers` is installed
   - Check middleware order in settings.py
   - Verify CORS settings are properly configured
   - Test with the provided `test_cors.html` file

### Logs
- Django logs: Check console output when running server
- Database logs: `docker-compose logs db`

## Contributing

1. Follow Django conventions and best practices
2. Use Django ORM instead of raw SQL
3. Implement proper error handling in API endpoints
4. Add tests for new features
5. Update documentation for API changes
6. Test CORS functionality when adding new endpoints 