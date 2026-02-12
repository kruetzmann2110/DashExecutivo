"""
Generate Sample Data for Executive Dashboard
This script creates CSV files with sample data for testing the dashboard
"""

import csv
import random
from datetime import datetime, timedelta

# Configuration
NUM_DEPARTMENTS = 10
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 200
NUM_SALES_RECORDS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

def generate_time_dimension():
    """Generate time dimension data"""
    time_data = []
    current_date = START_DATE
    time_key = 1
    
    while current_date <= END_DATE:
        time_data.append({
            'TimeKey': time_key,
            'Date': current_date.strftime('%Y-%m-%d'),
            'Year': current_date.year,
            'Quarter': (current_date.month - 1) // 3 + 1,
            'Month': current_date.month,
            'MonthName': current_date.strftime('%B'),
            'Week': current_date.isocalendar()[1],
            'DayOfMonth': current_date.day,
            'DayOfWeek': current_date.weekday(),
            'DayName': current_date.strftime('%A'),
            'IsWeekend': 1 if current_date.weekday() >= 5 else 0,
            'IsHoliday': 0  # Simplified
        })
        current_date += timedelta(days=1)
        time_key += 1
    
    return time_data

def generate_departments():
    """Generate department dimension data"""
    departments = [
        'Sales', 'Marketing', 'Operations', 'Finance', 'IT',
        'HR', 'Customer Service', 'R&D', 'Legal', 'Administration'
    ]
    managers = [
        'John Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Costa', 'Pedro Alves',
        'Julia Fernandes', 'Roberto Lima', 'Fernanda Rocha', 'Lucas Martins', 'Patricia Souza'
    ]
    
    dept_data = []
    for i, dept in enumerate(departments[:NUM_DEPARTMENTS], 1):
        dept_data.append({
            'DepartmentKey': i,
            'DepartmentID': f'DEPT{i:03d}',
            'DepartmentName': dept,
            'DepartmentCategory': 'Core Business' if i <= 5 else 'Support',
            'ManagerName': managers[i-1],
            'CostCenter': f'CC{i:03d}'
        })
    
    return dept_data

def generate_products():
    """Generate product dimension data"""
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home & Garden']
    brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
    
    product_data = []
    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(categories)
        product_data.append({
            'ProductKey': i,
            'ProductID': f'PROD{i:04d}',
            'ProductName': f'Product {i} - {category}',
            'Category': category,
            'SubCategory': f'Sub{category[:3]}{random.randint(1, 5)}',
            'Brand': random.choice(brands),
            'UnitPrice': round(random.uniform(10, 500), 2)
        })
    
    return product_data

def generate_customers():
    """Generate customer dimension data"""
    regions = ['North', 'South', 'East', 'West', 'Central']
    countries = ['Brazil', 'USA', 'Canada', 'Mexico', 'Argentina']
    cities = ['São Paulo', 'Rio de Janeiro', 'New York', 'Toronto', 'Mexico City']
    segments = ['Premium', 'Standard', 'Basic']
    
    customer_data = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customer_data.append({
            'CustomerKey': i,
            'CustomerID': f'CUST{i:05d}',
            'CustomerName': f'Customer {i}',
            'CustomerType': random.choice(['B2B', 'B2C']),
            'Segment': random.choice(segments),
            'Region': random.choice(regions),
            'Country': random.choice(countries),
            'City': random.choice(cities)
        })
    
    return customer_data

def generate_sales(time_data, products, customers, departments):
    """Generate sales fact data"""
    sales_data = []
    
    for i in range(1, NUM_SALES_RECORDS + 1):
        time_record = random.choice(time_data)
        product = random.choice(products)
        customer = random.choice(customers)
        department = random.choice(departments)
        
        quantity = random.randint(1, 20)
        unit_price = float(product['UnitPrice'])
        total_amount = quantity * unit_price
        discount_rate = random.choice([0, 0.05, 0.1, 0.15, 0.2])
        discount_amount = total_amount * discount_rate
        net_amount = total_amount - discount_amount
        cost_amount = net_amount * random.uniform(0.4, 0.7)
        profit_amount = net_amount - cost_amount
        
        sales_data.append({
            'SalesKey': i,
            'TimeKey': time_record['TimeKey'],
            'ProductKey': product['ProductKey'],
            'CustomerKey': customer['CustomerKey'],
            'DepartmentKey': department['DepartmentKey'],
            'Quantity': quantity,
            'UnitPrice': round(unit_price, 2),
            'TotalAmount': round(total_amount, 2),
            'DiscountAmount': round(discount_amount, 2),
            'NetAmount': round(net_amount, 2),
            'CostAmount': round(cost_amount, 2),
            'ProfitAmount': round(profit_amount, 2)
        })
    
    return sales_data

def generate_budget(time_data, departments):
    """Generate budget fact data"""
    budget_data = []
    budget_key = 1
    
    for dept in departments:
        for time_record in time_data:
            # Generate monthly budgets only
            if time_record['DayOfMonth'] == 1:
                budget_data.append({
                    'BudgetKey': budget_key,
                    'TimeKey': time_record['TimeKey'],
                    'DepartmentKey': dept['DepartmentKey'],
                    'BudgetAmount': round(random.uniform(50000, 500000), 2),
                    'BudgetType': random.choice(['Operational', 'Strategic', 'Investment'])
                })
                budget_key += 1
    
    return budget_data

def generate_kpis(time_data, departments):
    """Generate KPI fact data"""
    kpi_names = [
        'Customer Satisfaction', 'Employee Engagement', 'Process Efficiency',
        'Quality Score', 'Innovation Index'
    ]
    
    kpi_data = []
    kpi_key = 1
    
    for dept in departments:
        for kpi_name in kpi_names:
            for time_record in time_data:
                # Generate monthly KPIs only
                if time_record['DayOfMonth'] == 1:
                    target = random.uniform(70, 100)
                    value = target * random.uniform(0.8, 1.1)
                    
                    kpi_data.append({
                        'KPIKey': kpi_key,
                        'TimeKey': time_record['TimeKey'],
                        'DepartmentKey': dept['DepartmentKey'],
                        'KPIName': kpi_name,
                        'KPIValue': round(value, 2),
                        'KPITarget': round(target, 2),
                        'KPIUnit': '%'
                    })
                    kpi_key += 1
    
    return kpi_data

def write_csv(filename, data, fieldnames):
    """Write data to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f'Generated {filename} with {len(data)} records')

def main():
    """Main function to generate all sample data"""
    print('Generating sample data for Executive Dashboard...')
    
    # Generate dimensions
    time_data = generate_time_dimension()
    departments = generate_departments()
    products = generate_products()
    customers = generate_customers()
    
    # Generate facts
    sales_data = generate_sales(time_data, products, customers, departments)
    budget_data = generate_budget(time_data, departments)
    kpi_data = generate_kpis(time_data, departments)
    
    # Write to CSV files
    write_csv('DimTime.csv', time_data, 
              ['TimeKey', 'Date', 'Year', 'Quarter', 'Month', 'MonthName', 
               'Week', 'DayOfMonth', 'DayOfWeek', 'DayName', 'IsWeekend', 'IsHoliday'])
    
    write_csv('DimDepartment.csv', departments,
              ['DepartmentKey', 'DepartmentID', 'DepartmentName', 'DepartmentCategory', 
               'ManagerName', 'CostCenter'])
    
    write_csv('DimProduct.csv', products,
              ['ProductKey', 'ProductID', 'ProductName', 'Category', 
               'SubCategory', 'Brand', 'UnitPrice'])
    
    write_csv('DimCustomer.csv', customers,
              ['CustomerKey', 'CustomerID', 'CustomerName', 'CustomerType', 
               'Segment', 'Region', 'Country', 'City'])
    
    write_csv('FactSales.csv', sales_data,
              ['SalesKey', 'TimeKey', 'ProductKey', 'CustomerKey', 'DepartmentKey',
               'Quantity', 'UnitPrice', 'TotalAmount', 'DiscountAmount', 'NetAmount',
               'CostAmount', 'ProfitAmount'])
    
    write_csv('FactBudget.csv', budget_data,
              ['BudgetKey', 'TimeKey', 'DepartmentKey', 'BudgetAmount', 'BudgetType'])
    
    write_csv('FactKPI.csv', kpi_data,
              ['KPIKey', 'TimeKey', 'DepartmentKey', 'KPIName', 
               'KPIValue', 'KPITarget', 'KPIUnit'])
    
    print('Sample data generation completed successfully!')

if __name__ == '__main__':
    main()
