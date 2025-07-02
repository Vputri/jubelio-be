from django.urls import path
from . import views

app_name = 'supermarket'
 
urlpatterns = [
    path('api/most-sold-products/', views.most_sold_products, name='most_sold_products'),
    path('api/discount-quantity-correlation/', views.discount_quantity_correlation, name='discount_quantity_correlation'),
    path('api/quantity-by-country/', views.quantity_by_country, name='quantity_by_country'),
    path('api/filter-options/', views.filter_options, name='filter_options'),
] 