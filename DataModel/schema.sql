-- Executive Dashboard Data Model Schema
-- This SQL script defines the data model for the Executive Dashboard

-- Dimension: Time
CREATE TABLE DimTime (
    TimeKey INT PRIMARY KEY,
    Date DATE NOT NULL,
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    MonthName VARCHAR(20) NOT NULL,
    Week INT NOT NULL,
    DayOfMonth INT NOT NULL,
    DayOfWeek INT NOT NULL,
    DayName VARCHAR(20) NOT NULL,
    IsWeekend BIT NOT NULL,
    IsHoliday BIT NOT NULL
);

-- Dimension: Department
CREATE TABLE DimDepartment (
    DepartmentKey INT PRIMARY KEY,
    DepartmentID VARCHAR(20) NOT NULL,
    DepartmentName VARCHAR(100) NOT NULL,
    DepartmentCategory VARCHAR(50),
    ManagerName VARCHAR(100),
    CostCenter VARCHAR(20)
);

-- Dimension: Product
CREATE TABLE DimProduct (
    ProductKey INT PRIMARY KEY,
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(200) NOT NULL,
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    Brand VARCHAR(100),
    UnitPrice DECIMAL(18, 2)
);

-- Dimension: Customer
CREATE TABLE DimCustomer (
    CustomerKey INT PRIMARY KEY,
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(200) NOT NULL,
    CustomerType VARCHAR(50),
    Segment VARCHAR(50),
    Region VARCHAR(100),
    Country VARCHAR(100),
    City VARCHAR(100)
);

-- Fact: Sales
CREATE TABLE FactSales (
    SalesKey INT PRIMARY KEY,
    TimeKey INT NOT NULL,
    ProductKey INT NOT NULL,
    CustomerKey INT NOT NULL,
    DepartmentKey INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    TotalAmount DECIMAL(18, 2) NOT NULL,
    DiscountAmount DECIMAL(18, 2),
    NetAmount DECIMAL(18, 2) NOT NULL,
    CostAmount DECIMAL(18, 2),
    ProfitAmount DECIMAL(18, 2),
    FOREIGN KEY (TimeKey) REFERENCES DimTime(TimeKey),
    FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (DepartmentKey) REFERENCES DimDepartment(DepartmentKey)
);

-- Fact: Budget
CREATE TABLE FactBudget (
    BudgetKey INT PRIMARY KEY,
    TimeKey INT NOT NULL,
    DepartmentKey INT NOT NULL,
    BudgetAmount DECIMAL(18, 2) NOT NULL,
    BudgetType VARCHAR(50),
    FOREIGN KEY (TimeKey) REFERENCES DimTime(TimeKey),
    FOREIGN KEY (DepartmentKey) REFERENCES DimDepartment(DepartmentKey)
);

-- Fact: KPIs
CREATE TABLE FactKPI (
    KPIKey INT PRIMARY KEY,
    TimeKey INT NOT NULL,
    DepartmentKey INT NOT NULL,
    KPIName VARCHAR(100) NOT NULL,
    KPIValue DECIMAL(18, 2) NOT NULL,
    KPITarget DECIMAL(18, 2),
    KPIUnit VARCHAR(20),
    FOREIGN KEY (TimeKey) REFERENCES DimTime(TimeKey),
    FOREIGN KEY (DepartmentKey) REFERENCES DimDepartment(DepartmentKey)
);
