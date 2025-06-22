#!/usr/bin/env python3
"""
Test script for the supermarket API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/supermarket"

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
    test_api_endpoint("/api/most-sold-products/", "Most Sold Products (Pie Chart Data)")
    test_api_endpoint("/api/discount-quantity-correlation/", "Discount vs Quantity Correlation (Scatter Plot Facet)")
    test_api_endpoint("/api/quantity-by-country/", "Quantity by Country (Heatmap Data)")

if __name__ == "__main__":
    main() 