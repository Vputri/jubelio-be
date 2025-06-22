from django.contrib import admin
from .models import Category, SubCategory, Product, Sales, InventoryMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'category__name']
    ordering = ['category__name', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sub_category', 'manufacturer', 'created_at']
    list_filter = ['category', 'sub_category', 'manufacturer']
    search_fields = ['name', 'manufacturer']
    ordering = ['name']


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_date', 'customer_name', 'product', 'quantity', 'sales_amount', 'country', 'state']
    list_filter = ['order_date', 'country', 'state', 'segment', 'ship_mode']
    search_fields = ['order_id', 'customer_name', 'product__name']
    date_hierarchy = 'order_date'
    ordering = ['-order_date']


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'movement_date', 'reference']
    list_filter = ['movement_type', 'movement_date', 'product__category']
    search_fields = ['product__name', 'reference']
    date_hierarchy = 'movement_date'
    ordering = ['-movement_date']
