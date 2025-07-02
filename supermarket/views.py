from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg, F
from django.views.decorators.http import require_http_methods
from decimal import Decimal
import json
from .models import Sales, Product, Category, SubCategory
from rest_framework.decorators import api_view


@api_view(['GET'])
def most_sold_products(request):
    """
    API endpoint to get the most sold products to least sold products (for Pie Chart)
    
    Query Parameters (opsional):
    - category: Nama kategori (contoh: Technology)
    - subcategory: Nama subkategori (contoh: Chairs)
    - country: Nama negara
    - city: Nama kota
    - state: Nama provinsi/wilayah
    - region: Nama region
    
    Returns data in format suitable for pie chart visualization
    """
    try:
        # Ambil filter dari query params
        filters = {}
        if 'category' in request.GET:
            filters['product__category__name'] = request.GET['category']
        if 'subcategory' in request.GET:
            filters['product__sub_category__name'] = request.GET['subcategory']
        if 'country' in request.GET:
            filters['country'] = request.GET['country']
        if 'city' in request.GET:
            filters['city'] = request.GET['city']
        if 'state' in request.GET:
            filters['state'] = request.GET['state']
        if 'region' in request.GET:
            filters['region'] = request.GET['region']

        # Get total quantity sold for each product dengan filter
        product_sales = Sales.objects.filter(**filters).values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')
        
        # Format data for pie chart
        pie_data = {
            'labels': [],
            'data': [],
            'total_sales': 0
        }
        
        for item in product_sales:
            pie_data['labels'].append(item['product__name'])
            pie_data['data'].append(item['total_quantity'])
            pie_data['total_sales'] += item['total_quantity']
        
        response = JsonResponse({
            'success': True,
            'data': pie_data,
            'message': 'Most sold products data retrieved successfully'
        })
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
        
    except Exception as e:
        response = JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error retrieving most sold products data'
        }, status=500)
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response


@api_view(['GET'])
def discount_quantity_correlation(request):
    """
    API endpoint to get correlation between discount (y) and quantity sales (x) based on state (facet)
    
    Query Parameters (opsional):
    - category: Nama kategori (contoh: Technology)
    - subcategory: Nama subkategori (contoh: Chairs)
    - country: Nama negara
    - city: Nama kota
    - state: Nama provinsi/wilayah
    - region: Nama region
    
    Returns data suitable for scatter plot facet chart
    """
    try:
        # Ambil filter dari query params
        filters = {}
        if 'category' in request.GET:
            filters['product__category__name'] = request.GET['category']
        if 'subcategory' in request.GET:
            filters['product__sub_category__name'] = request.GET['subcategory']
        if 'country' in request.GET:
            filters['country'] = request.GET['country']
        if 'city' in request.GET:
            filters['city'] = request.GET['city']
        if 'region' in request.GET:
            filters['region'] = request.GET['region']

        # Get discount vs quantity data grouped by state dengan filter
        correlation_data = Sales.objects.filter(**filters).values(
            'state'
        ).annotate(
            avg_discount=Avg('discount'),
            avg_quantity=Avg('quantity'),
            total_records=Count('id')
        ).filter(
            total_records__gte=5  # Only include states with at least 5 records for meaningful correlation
        ).order_by('state')
        
        # Format data for scatter plot facet chart
        facet_data = {
            'states': [],
            'correlations': []
        }
        
        for item in correlation_data:
            # Get individual points for this state dengan filter
            state_points = Sales.objects.filter(state=item['state'], **filters).values('discount', 'quantity')
            
            points = []
            for point in state_points:
                points.append({
                    'x': float(point['quantity']),
                    'y': float(point['discount'])
                })
            
            facet_data['states'].append(item['state'])
            facet_data['correlations'].append({
                'state': item['state'],
                'avg_discount': float(item['avg_discount']),
                'avg_quantity': float(item['avg_quantity']),
                'total_records': item['total_records'],
                'points': points
            })
        
        response = JsonResponse({
            'success': True,
            'data': facet_data,
            'message': 'Discount vs quantity correlation data retrieved successfully'
        })
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
        
    except Exception as e:
        response = JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error retrieving discount vs quantity correlation data'
        }, status=500)
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response


@api_view(['GET'])
def quantity_by_country(request):
    """
    API endpoint to get quantity sold by country (heatmap chart)
    
    Query Parameters (opsional):
    - category: Nama kategori (contoh: Technology)
    - subcategory: Nama subkategori (contoh: Chairs)
    - country: Nama negara
    - city: Nama kota
    - state: Nama provinsi/wilayah
    - region: Nama region
    
    Returns data suitable for heatmap visualization
    """
    try:
        # Ambil filter dari query params
        filters = {}
        if 'category' in request.GET:
            filters['product__category__name'] = request.GET['category']
        if 'subcategory' in request.GET:
            filters['product__sub_category__name'] = request.GET['subcategory']
        if 'state' in request.GET:
            filters['state'] = request.GET['state']
        if 'city' in request.GET:
            filters['city'] = request.GET['city']
        if 'region' in request.GET:
            filters['region'] = request.GET['region']

        # Get quantity sold by country and category for heatmap dengan filter
        heatmap_data = Sales.objects.filter(**filters).values(
            'country',
            'product__category__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('country', 'product__category__name')
        
        # Format data for heatmap
        countries = []
        categories = []
        data_matrix = {}
        
        # Collect unique countries and categories
        for item in heatmap_data:
            country = item['country']
            category = item['product__category__name']
            
            if country not in countries:
                countries.append(country)
            
            if category not in categories:
                categories.append(category)
            
            # Store data in matrix format
            if country not in data_matrix:
                data_matrix[country] = {}
            data_matrix[country][category] = item['total_quantity']
        
        # Create heatmap data array
        heatmap_array = []
        for country in countries:
            for category in categories:
                quantity = data_matrix.get(country, {}).get(category, 0)
                heatmap_array.append({
                    'country': country,
                    'category': category,
                    'quantity': quantity
                })
        
        heatmap_data = {
            'countries': countries,
            'categories': categories,
            'data': heatmap_array,
            'matrix': data_matrix
        }
        
        response = JsonResponse({
            'success': True,
            'data': heatmap_data,
            'message': 'Quantity by country data retrieved successfully'
        })
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
        
    except Exception as e:
        response = JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Error retrieving quantity by country data'
        }, status=500)
        
        # Add CORS headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response


@api_view(['GET'])
def filter_options(request):
    """
    API endpoint untuk mendapatkan daftar nilai unik untuk filter:
    - category
    - subcategory
    - country
    - city
    - state
    - region
    """
    categories = list(Category.objects.order_by('name').values_list('name', flat=True))
    subcategories = list(SubCategory.objects.order_by('name').values_list('name', flat=True))
    countries = list(Sales.objects.order_by('country').values_list('country', flat=True).distinct())
    cities = list(Sales.objects.order_by('city').values_list('city', flat=True).distinct())
    states = list(Sales.objects.order_by('state').values_list('state', flat=True).distinct())
    regions = list(Sales.objects.order_by('region').values_list('region', flat=True).distinct())
    return JsonResponse({
        'success': True,
        'data': {
            'categories': categories,
            'subcategories': subcategories,
            'countries': countries,
            'cities': cities,
            'states': states,
            'regions': regions,
        },
        'message': 'Filter options retrieved successfully'
    })
