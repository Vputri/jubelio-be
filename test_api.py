#!/usr/bin/env python3
"""
Test script for the supermarket API endpoints

Endpoint yang diuji:
- /most-sold-products/
- /discount-quantity-correlation/
- /quantity-by-country/
- /filter-options/ (mengembalikan daftar unik untuk filter: category, subcategory, country, city, state, region)
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/supermarket/api/'

def test_api_endpoint(endpoint, description):
    """Test an API endpoint and print results"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Endpoint: {BASE_URL}{endpoint}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Django is running on localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Supermarket API Test Script")
    print("Make sure Django server is running: python manage.py runserver")
    
    # Test endpoints
    test_api_endpoint("most-sold-products/", "Most Sold Products (Pie Chart Data)")
    test_api_endpoint("discount-quantity-correlation/", "Discount vs Quantity Correlation (Scatter Plot Facet)")
    test_api_endpoint("quantity-by-country/", "Quantity by Country (Heatmap Data)")
    test_api_endpoint("filter-options/", "Filter Options (List for Filter Dropdown)")

    print('--- TEST: Most Sold Products (tanpa filter) ---')
    print_response(requests.get(BASE_URL + 'most-sold-products/'), 'Most Sold Products (tanpa filter)')

    print('--- TEST: Most Sold Products (filter category=Technology, country=Indonesia) ---')
    print_response(requests.get(BASE_URL + 'most-sold-products/', params={'category': 'Technology', 'country': 'Indonesia'}), 'Most Sold Products (filter category=Technology, country=Indonesia)')

    print('--- TEST: Discount-Quantity Correlation (filter subcategory=Chairs, state=Jawa Barat) ---')
    print_response(requests.get(BASE_URL + 'discount-quantity-correlation/', params={'subcategory': 'Chairs', 'state': 'Jawa Barat'}), 'Discount-Quantity Correlation (filter subcategory=Chairs, state=Jawa Barat)')

    print('--- TEST: Quantity by Country (filter region=Asia, city=Jakarta) ---')
    print_response(requests.get(BASE_URL + 'quantity-by-country/', params={'region': 'Asia', 'city': 'Jakarta'}), 'Quantity by Country (filter region=Asia, city=Jakarta)')

def print_response(r, label=None):
    if label:
        print(f'--- TEST: {label} ---')
    try:
        r.raise_for_status()
        print(r.json())
    except requests.exceptions.HTTPError as e:
        print(f'HTTP error: {e} (status code: {r.status_code})')
        print(r.text)
    except Exception as e:
        print(f'Error decoding JSON: {e} (status code: {r.status_code})')
        print(r.text)

if __name__ == "__main__":
    main() 