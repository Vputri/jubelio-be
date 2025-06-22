import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import re
from supermarket.models import Category, SubCategory, Product, Sales, InventoryMovement


class Command(BaseCommand):
    help = 'Import data from Excel file to PostgreSQL database'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def clean_currency(self, value):
        """Clean currency values by removing $ and converting to Decimal"""
        if pd.isna(value):
            return Decimal('0.00')
        
        if isinstance(value, str):
            # Remove $ and any other non-numeric characters except decimal point
            cleaned = re.sub(r'[^\d.-]', '', value)
            try:
                return Decimal(cleaned)
            except:
                return Decimal('0.00')
        elif isinstance(value, (int, float)):
            return Decimal(str(value))
        else:
            return Decimal('0.00')

    def clean_discount(self, value):
        """Clean discount values and convert to decimal between 0 and 1"""
        if pd.isna(value):
            return Decimal('0.00')
        
        if isinstance(value, str):
            # Remove % and convert to decimal
            cleaned = re.sub(r'[^\d.-]', '', value)
            try:
                discount = Decimal(cleaned)
                # If it's a percentage (e.g., 20%), convert to decimal (0.20)
                if discount > 1:
                    discount = discount / 100
                return discount
            except:
                return Decimal('0.00')
        elif isinstance(value, (int, float)):
            discount = Decimal(str(value))
            if discount > 1:
                discount = discount / 100
            return discount
        else:
            return Decimal('0.00')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        try:
            # Read Excel file
            self.stdout.write(f"Reading Excel file: {excel_file}")
            df = pd.read_excel(excel_file)
            self.stdout.write(f"Found {len(df)} rows in the dataset")
            
            with transaction.atomic():
                # Clear existing data
                self.stdout.write("Clearing existing data...")
                Sales.objects.all().delete()
                InventoryMovement.objects.all().delete()
                Product.objects.all().delete()
                SubCategory.objects.all().delete()
                Category.objects.all().delete()
                
                # Import Categories and SubCategories
                self.stdout.write("Importing Categories and SubCategories...")
                category_subcategory_map = {}
                
                for _, row in df.iterrows():
                    category_name = row['Category']
                    subcategory_name = row['Sub-Category']
                    
                    if category_name not in category_subcategory_map:
                        category, created = Category.objects.get_or_create(name=category_name)
                        category_subcategory_map[category_name] = {}
                    
                    if subcategory_name not in category_subcategory_map[category_name]:
                        subcategory, created = SubCategory.objects.get_or_create(
                            name=subcategory_name,
                            category=category_subcategory_map[category_name].get('category', category)
                        )
                        category_subcategory_map[category_name][subcategory_name] = subcategory
                        category_subcategory_map[category_name]['category'] = category
                
                self.stdout.write(f"Created {Category.objects.count()} categories and {SubCategory.objects.count()} subcategories")
                
                # Import Products
                self.stdout.write("Importing Products...")
                product_map = {}
                
                for _, row in df.iterrows():
                    product_name = row['Product Name']
                    category_name = row['Category']
                    subcategory_name = row['Sub-Category']
                    manufacturer = row['Manufacturer']
                    
                    if product_name not in product_map:
                        category = category_subcategory_map[category_name]['category']
                        subcategory = category_subcategory_map[category_name][subcategory_name]
                        
                        product, created = Product.objects.get_or_create(
                            name=product_name,
                            defaults={
                                'category': category,
                                'sub_category': subcategory,
                                'manufacturer': manufacturer
                            }
                        )
                        product_map[product_name] = product
                
                self.stdout.write(f"Created {Product.objects.count()} products")
                
                # Import Sales
                self.stdout.write("Importing Sales...")
                sales_count = 0
                
                for _, row in df.iterrows():
                    try:
                        product = product_map[row['Product Name']]
                        
                        # Clean and convert data
                        sales_amount = self.clean_currency(row['Sales'])
                        profit = self.clean_currency(row['Profit'])
                        discount = self.clean_discount(row['Discount'])
                        profit_ratio = self.clean_currency(row['Profit Ratio'])
                        
                        # Create sales record
                        sales, created = Sales.objects.get_or_create(
                            order_id=row['Order ID'],
                            defaults={
                                'order_date': pd.to_datetime(row['Order Date']).date(),
                                'ship_date': pd.to_datetime(row['Ship Date']).date(),
                                'ship_mode': row['Ship Mode'],
                                'customer_name': row['Customer Name'],
                                'segment': row['Segment'],
                                'country': row['Country'],
                                'city': row['City'],
                                'state': row['State'],
                                'postal_code': str(row['Postal Code']),
                                'region': row['Region'],
                                'product': product,
                                'quantity': int(row['Quantity']),
                                'sales_amount': sales_amount,
                                'discount': discount,
                                'profit': profit,
                                'profit_ratio': profit_ratio,
                            }
                        )
                        
                        if created:
                            sales_count += 1
                            
                            # Create inventory movement (OUT) for sales
                            InventoryMovement.objects.create(
                                product=product,
                                movement_type='OUT',
                                quantity=int(row['Quantity']),
                                movement_date=pd.to_datetime(row['Order Date']).date(),
                                reference=row['Order ID']
                            )
                    
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Error processing row: {e}"))
                        continue
                
                self.stdout.write(f"Created {sales_count} sales records")
                self.stdout.write(f"Created {InventoryMovement.objects.count()} inventory movements")
                
                self.stdout.write(self.style.SUCCESS("Data import completed successfully!"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
            raise 