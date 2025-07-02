# 🛒 Sistem Analisis Data Supermarket - Django & PostgreSQL

Proyek backend untuk analisis data supermarket menggunakan Django dan PostgreSQL. Sistem ini mengolah data Excel Kaggle dan menyediakan API untuk visualisasi data.

## 📊 Dataset

- **Sumber**: Kaggle Supermarket Dataset
- **Ukuran**: 9,994 records dengan 21 kolom
- **Format**: Excel (.xlsx)
- **Kategori**: 3 kategori utama (Technology, Furniture, Office Supplies)

## 🏗️ Arsitektur Sistem

```
Excel Dataset → Django App → PostgreSQL → REST API → Frontend Visualization
```

## 🛠️ Teknologi Stack

### Backend
- **Django 5.2.3** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Pandas** - Data processing
- **OpenPyXL** - Excel file handling

### Development Tools
- **Docker** - Containerization
- **Swagger/OpenAPI** - API documentation
- **django-cors-headers** - CORS support

## 📁 Struktur Proyek

```
jubelio/
├── jubelio/                 # Django project settings
├── supermarket/            # Main app
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin interface
├── management/            # Custom commands
│   └── commands/
│       └── import_data.py # Data import command
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Docker configuration
├── manage.py             # Django management
└── README.md             # Documentation
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd jubelio

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Start PostgreSQL with Docker
docker-compose up -d

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Import Data

```bash
# Import Excel data to PostgreSQL
python manage.py import_data
```

### 4. Run Server

```bash
# Start development server
python manage.py runserver

# Server will be available at http://localhost:8000
```

## 📊 API Endpoints

### 1. Most Sold Products (Pie Chart)
```
GET /api/most-sold-products/
```
**Response**: Data untuk pie chart produk terlaris

### 2. Discount vs Quantity Correlation (Scatter Plot)
```
GET /api/discount-correlation/
```
**Response**: Data korelasi diskon vs kuantitas per negara bagian

### 3. Quantity Sold by Country (Heatmap)
```
GET /api/quantity-by-country/
```
**Response**: Data penjualan per negara dan kategori

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## 🧪 Testing

### API Testing
```bash
# Run test script
python test_api.py
```

### CORS Testing
1. Buka `test_cors.html` di browser
2. Klik tombol "Test API"
3. Periksa response di console

## 📈 Data Models

### Category
- `name` - Nama kategori (Technology, Furniture, Office Supplies)

### SubCategory
- `name` - Nama sub-kategori
- `category` - Foreign key ke Category

### Product
- `name` - Nama produk
- `subcategory` - Foreign key ke SubCategory
- `unit_price` - Harga per unit

### Sales
- `product` - Foreign key ke Product
- `quantity` - Kuantitas terjual
- `discount` - Diskon (0-1)
- `profit` - Profit
- `state` - Negara bagian
- `region` - Region
- `date` - Tanggal penjualan

### InventoryMovement
- `product` - Foreign key ke Product
- `movement_type` - Jenis pergerakan (IN/OUT)
- `quantity` - Kuantitas
- `date` - Tanggal pergerakan

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/supermarket

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### CORS Settings
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

## 📊 Data Insights

### Top Categories
1. **Technology** - 37% dari total penjualan
2. **Furniture** - 33% dari total penjualan  
3. **Office Supplies** - 30% dari total penjualan

### Key Metrics
- **Total Products**: 1,850 produk unik
- **Total Sales**: 5,009 transaksi
- **Date Range**: 2014-2017
- **Geographic Coverage**: 49 negara bagian

## 🎯 Business Value

### Analytics Capabilities
- **Product Performance Analysis** - Identifikasi produk terlaris
- **Pricing Optimization** - Analisis korelasi diskon
- **Geographic Insights** - Penjualan per wilayah
- **Trend Analysis** - Pola penjualan temporal

### Strategic Benefits
- **Data-Driven Decisions** - Berbasis data untuk strategi bisnis
- **Market Expansion** - Identifikasi pasar potensial
- **Inventory Management** - Optimasi stok berdasarkan penjualan
- **Pricing Strategy** - Penetapan harga optimal

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build
```

### Production Setup
1. Set `DEBUG=False`
2. Configure production database
3. Set up static files serving
4. Configure HTTPS
5. Set up monitoring

## 📝 Development

### Adding New Endpoints
1. Create view in `views.py`
2. Add URL pattern in `urls.py`
3. Update API documentation
4. Add tests

### Data Import Process
1. Place Excel file in project root
2. Run `python manage.py import_data`
3. Verify data in admin interface

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Contact

- **Name**: Vika Putri Ariyanti
- **Email**: vikaputriariyanti@gmail.com
- **LinkedIn**: [linkedin.com/in/vikaputriariyanti](https://www.linkedin.com/in/vikaputriariyanti/)
- **GitHub**: [github.com/Vputri](https://github.com/Vputri)

---

## 📋 Checklist Setup

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] PostgreSQL running
- [ ] Database migrations applied
- [ ] Data imported successfully
- [ ] Server running on localhost:8000
- [ ] API endpoints accessible
- [ ] Swagger documentation working
- [ ] CORS testing successful

## 🎯 Next Steps

1. **Frontend Development** - Dashboard visualization
2. **Advanced Analytics** - Machine learning integration
3. **Real-time Updates** - WebSocket implementation
4. **Mobile App** - React Native integration
5. **Cloud Deployment** - AWS/Azure setup

---

**Happy Coding! 🚀**

## 📋 Konversi Slide ke HTML

Untuk mengubah slide presentasi ke format HTML:

```bash
python markdown_to_html.py SLIDE_PRESENTASI.md slide_presentasi.html
```

File HTML dapat dibuka di browser untuk presentasi. 