# Sample Data Generator

This directory contains a Python script to generate sample data for testing the Executive Dashboard.

## Usage

Run the script to generate CSV files with sample data:

```bash
python generate_sample_data.py
```

## Generated Files

The script will create the following CSV files:

- **DimTime.csv** - Time dimension (731 records for 2023-2024)
- **DimDepartment.csv** - Department dimension (10 records)
- **DimProduct.csv** - Product dimension (50 records)
- **DimCustomer.csv** - Customer dimension (200 records)
- **FactSales.csv** - Sales fact table (5000 records)
- **FactBudget.csv** - Budget fact table (240 records)
- **FactKPI.csv** - KPI fact table (1200 records)

## Customization

You can modify the following constants at the top of the script to change the data volume:

```python
NUM_DEPARTMENTS = 10        # Number of departments
NUM_PRODUCTS = 50           # Number of products
NUM_CUSTOMERS = 200         # Number of customers
NUM_SALES_RECORDS = 5000    # Number of sales transactions
START_DATE = datetime(2023, 1, 1)  # Start date for time dimension
END_DATE = datetime(2024, 12, 31)  # End date for time dimension
```

## Data Characteristics

The generated data includes:

- **Realistic relationships** between dimensions and facts
- **Random but plausible values** for sales, budgets, and KPIs
- **Date coverage** from 2023 to 2024 (2 years)
- **Varied product categories**: Electronics, Clothing, Food, Books, Home & Garden
- **Multiple customer segments**: Premium, Standard, Basic
- **Different customer types**: B2B, B2C
- **Various regions**: North, South, East, West, Central

## Importing to Database

After generating the CSV files, you can import them to your database:

### SQL Server (using BCP):
```bash
bcp DatabaseName.dbo.DimTime in DimTime.csv -c -t, -S ServerName -U Username -P Password
bcp DatabaseName.dbo.DimDepartment in DimDepartment.csv -c -t, -S ServerName -U Username -P Password
# ... repeat for all tables
```

### SQL Server (using BULK INSERT):
```sql
BULK INSERT DimTime
FROM 'C:\path\to\DimTime.csv'
WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');
```

### Power BI Desktop:
1. Open Power BI Desktop
2. Get Data > Text/CSV
3. Browse to each CSV file and load
4. Establish relationships in Model view

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## Notes

- CSV files are excluded from git via .gitignore
- Each run will overwrite existing CSV files
- Data is randomly generated, so each run produces different values
- For production use, replace with actual data from your systems
