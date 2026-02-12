# Data Dictionary - Executive Dashboard

## Overview
This document describes all tables, columns, and their relationships in the Executive Dashboard data model.

---

## Dimension Tables

### DimTime
**Description**: Time dimension for date-based analysis

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| TimeKey | INT | Primary key, surrogate key for time | 1, 2, 3... |
| Date | DATE | Actual date | 2024-01-15 |
| Year | INT | Year | 2024 |
| Quarter | INT | Quarter (1-4) | 1 |
| Month | INT | Month number (1-12) | 1 |
| MonthName | VARCHAR(20) | Month name | January |
| Week | INT | Week number in year | 3 |
| DayOfMonth | INT | Day of month (1-31) | 15 |
| DayOfWeek | INT | Day of week (0=Monday, 6=Sunday) | 0 |
| DayName | VARCHAR(20) | Day name | Monday |
| IsWeekend | BIT | 1 if weekend, 0 otherwise | 0 |
| IsHoliday | BIT | 1 if holiday, 0 otherwise | 0 |

**Relationships**:
- Referenced by: FactSales, FactBudget, FactKPI

---

### DimDepartment
**Description**: Organizational departments dimension

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| DepartmentKey | INT | Primary key, surrogate key | 1, 2, 3... |
| DepartmentID | VARCHAR(20) | Department identifier | DEPT001 |
| DepartmentName | VARCHAR(100) | Department name | Sales |
| DepartmentCategory | VARCHAR(50) | Department category | Core Business |
| ManagerName | VARCHAR(100) | Department manager name | John Silva |
| CostCenter | VARCHAR(20) | Cost center code | CC001 |

**Relationships**:
- Referenced by: FactSales, FactBudget, FactKPI

**Business Rules**:
- Used for Row-Level Security filtering
- ManagerName can be used to filter data by manager

---

### DimProduct
**Description**: Product catalog dimension

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| ProductKey | INT | Primary key, surrogate key | 1, 2, 3... |
| ProductID | VARCHAR(20) | Product identifier | PROD0001 |
| ProductName | VARCHAR(200) | Product name | Product 1 - Electronics |
| Category | VARCHAR(100) | Product category | Electronics |
| SubCategory | VARCHAR(100) | Product subcategory | SubEle1 |
| Brand | VARCHAR(100) | Product brand | BrandA |
| UnitPrice | DECIMAL(18,2) | Standard unit price | 299.99 |

**Relationships**:
- Referenced by: FactSales

**Business Rules**:
- UnitPrice is the standard price; actual transaction prices in FactSales may vary

---

### DimCustomer
**Description**: Customer master data dimension

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| CustomerKey | INT | Primary key, surrogate key | 1, 2, 3... |
| CustomerID | VARCHAR(20) | Customer identifier | CUST00001 |
| CustomerName | VARCHAR(200) | Customer name | Customer 1 |
| CustomerType | VARCHAR(50) | Type of customer | B2B or B2C |
| Segment | VARCHAR(50) | Customer segment | Premium |
| Region | VARCHAR(100) | Geographic region | North |
| Country | VARCHAR(100) | Country | Brazil |
| City | VARCHAR(100) | City | São Paulo |

**Relationships**:
- Referenced by: FactSales

**Business Rules**:
- Region can be used for Row-Level Security
- Segment affects pricing and discounts

---

## Fact Tables

### FactSales
**Description**: Sales transaction fact table

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| SalesKey | INT | Primary key, surrogate key | 1, 2, 3... |
| TimeKey | INT | Foreign key to DimTime | 365 |
| ProductKey | INT | Foreign key to DimProduct | 25 |
| CustomerKey | INT | Foreign key to DimCustomer | 150 |
| DepartmentKey | INT | Foreign key to DimDepartment | 1 |
| Quantity | INT | Quantity sold | 5 |
| UnitPrice | DECIMAL(18,2) | Price per unit | 299.99 |
| TotalAmount | DECIMAL(18,2) | Quantity × UnitPrice | 1499.95 |
| DiscountAmount | DECIMAL(18,2) | Total discount applied | 149.99 |
| NetAmount | DECIMAL(18,2) | TotalAmount - DiscountAmount | 1349.96 |
| CostAmount | DECIMAL(18,2) | Total cost of goods | 809.98 |
| ProfitAmount | DECIMAL(18,2) | NetAmount - CostAmount | 539.98 |

**Relationships**:
- TimeKey → DimTime.TimeKey
- ProductKey → DimProduct.ProductKey
- CustomerKey → DimCustomer.CustomerKey
- DepartmentKey → DimDepartment.DepartmentKey

**Business Rules**:
- NetAmount is the primary metric for "Sales"
- ProfitAmount = NetAmount - CostAmount
- TotalAmount = Quantity × UnitPrice
- NetAmount = TotalAmount - DiscountAmount

**Grain**: One row per sales transaction line item

---

### FactBudget
**Description**: Department budget fact table

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| BudgetKey | INT | Primary key, surrogate key | 1, 2, 3... |
| TimeKey | INT | Foreign key to DimTime | 1 |
| DepartmentKey | INT | Foreign key to DimDepartment | 1 |
| BudgetAmount | DECIMAL(18,2) | Budgeted amount | 250000.00 |
| BudgetType | VARCHAR(50) | Type of budget | Operational |

**Relationships**:
- TimeKey → DimTime.TimeKey
- DepartmentKey → DimDepartment.DepartmentKey

**Business Rules**:
- Budget is typically set at monthly level
- BudgetType categories: Operational, Strategic, Investment

**Grain**: One row per department per month

---

### FactKPI
**Description**: Key Performance Indicators fact table

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| KPIKey | INT | Primary key, surrogate key | 1, 2, 3... |
| TimeKey | INT | Foreign key to DimTime | 1 |
| DepartmentKey | INT | Foreign key to DimDepartment | 1 |
| KPIName | VARCHAR(100) | Name of KPI | Customer Satisfaction |
| KPIValue | DECIMAL(18,2) | Actual KPI value | 87.50 |
| KPITarget | DECIMAL(18,2) | Target value for KPI | 85.00 |
| KPIUnit | VARCHAR(20) | Unit of measurement | % |

**Relationships**:
- TimeKey → DimTime.TimeKey
- DepartmentKey → DimDepartment.DepartmentKey

**Business Rules**:
- KPIs are typically measured at monthly level
- KPIValue vs KPITarget determines achievement status
- Common KPIs: Customer Satisfaction, Employee Engagement, Process Efficiency, Quality Score, Innovation Index

**Grain**: One row per KPI per department per month

---

## Relationships Diagram

```
DimTime ─────┬─────> FactSales
             ├─────> FactBudget
             └─────> FactKPI

DimDepartment ┬─────> FactSales
              ├─────> FactBudget
              └─────> FactKPI

DimProduct ──────────> FactSales

DimCustomer ─────────> FactSales
```

**Cardinality**: All relationships are Many-to-One (Fact to Dimension)
**Filter Direction**: Single direction (from Fact to Dimension)

---

## Data Quality Rules

### DimTime
- Must have continuous dates with no gaps
- Holiday flags should be updated annually

### DimDepartment
- Department names must be unique
- Each department must have a manager assigned

### DimProduct
- Product IDs must be unique
- UnitPrice must be greater than 0

### DimCustomer
- Customer IDs must be unique
- Region and Country fields are required for geographic analysis

### FactSales
- All foreign keys must have matching records in dimension tables
- NetAmount must equal TotalAmount - DiscountAmount
- ProfitAmount must equal NetAmount - CostAmount
- Quantity must be greater than 0

### FactBudget
- Budget amounts should be positive
- Each department should have budget for each month

### FactKPI
- KPI values and targets should be in appropriate ranges
- KPI names should be standardized across departments

---

## Performance Considerations

### Indexes
Recommended indexes for optimal performance:

**DimTime**:
- Clustered index on TimeKey
- Non-clustered index on Date

**FactSales**:
- Clustered index on SalesKey
- Non-clustered indexes on: TimeKey, ProductKey, CustomerKey, DepartmentKey

**FactBudget**:
- Clustered index on BudgetKey
- Non-clustered indexes on: TimeKey, DepartmentKey

**FactKPI**:
- Clustered index on KPIKey
- Non-clustered indexes on: TimeKey, DepartmentKey, KPIName

### Partitioning
For large datasets, consider partitioning fact tables by TimeKey:
- Annual partitions for historical data
- Monthly partitions for recent data

---

## Change History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2024-01-01 | 1.0 | Initial data dictionary | Dashboard Team |
