# Deployment Guide - Executive Dashboard

## Prerequisites

### Software Requirements:
- **Power BI Desktop**: Latest version (download from Microsoft Store or powerbi.microsoft.com)
- **Power BI Pro License**: Required for publishing to Power BI Service
- **Database Access**: Credentials for connecting to your data source

### Data Requirements:
- SQL Server, Azure SQL Database, or compatible data source
- Access permissions to read data
- Network connectivity to data source

---

## Step 1: Setup Data Source

### Option A: Using Sample Data (for testing)

1. **Generate Sample Data**:
   ```bash
   cd SampleData
   python generate_sample_data.py
   ```

2. **Import CSV files** into your database or use Power BI's "Get Data" > "Text/CSV" option

### Option B: Using Your Own Database

1. Ensure your database has tables matching the schema in `DataModel/schema.sql`
2. Run the schema script to create tables if needed:
   ```sql
   -- Execute schema.sql on your database
   ```

---

## Step 2: Create Power BI Report

### Method 1: Building from Scratch

1. **Open Power BI Desktop**

2. **Connect to Data Source**:
   - Click "Get Data"
   - Select your data source type (SQL Server, CSV, etc.)
   - Enter connection details
   - Load all dimension and fact tables

3. **Configure Data Model**:
   - Go to "Model" view
   - Create relationships:
     - FactSales[TimeKey] → DimTime[TimeKey]
     - FactSales[ProductKey] → DimProduct[ProductKey]
     - FactSales[CustomerKey] → DimCustomer[CustomerKey]
     - FactSales[DepartmentKey] → DimDepartment[DepartmentKey]
     - FactBudget[TimeKey] → DimTime[TimeKey]
     - FactBudget[DepartmentKey] → DimDepartment[DepartmentKey]
     - FactKPI[TimeKey] → DimTime[TimeKey]
     - FactKPI[DepartmentKey] → DimDepartment[DepartmentKey]
   
   - Set cardinality: Many-to-One (*:1)
   - Set cross-filter direction: Single (except where bidirectional is needed)

4. **Create Measures**:
   - Open "Data" view
   - Create a new table called "Measures"
   - Copy DAX measures from `DAX/measures.dax`
   - Paste each measure into Power BI

5. **Build Dashboard Pages**:
   - Follow specifications in `Documentation/dashboard_design.md`
   - Create 5 pages: Executive Overview, Financial Performance, Sales Analysis, Customer Insights, KPI Dashboard

6. **Add Slicers and Filters**:
   - Add date range slicer (synchronized across pages)
   - Add department, region, and category slicers as needed

7. **Format Visuals**:
   - Apply consistent color scheme (see dashboard_design.md)
   - Format numbers (currency, percentages)
   - Add data labels where appropriate

8. **Save the Report**:
   - File > Save As
   - Name: "Executive_Dashboard.pbix"

---

## Step 3: Configure Data Refresh

### For Power BI Service:

1. **Install Gateway** (if using on-premises data):
   - Download and install Power BI Gateway on a server
   - Configure gateway to access your data source
   - Register gateway in Power BI Service

2. **Configure Credentials**:
   - In Power BI Service, go to Dataset Settings
   - Under "Data source credentials", click "Edit credentials"
   - Enter database username and password
   - Set privacy level to "Organizational"

3. **Schedule Refresh**:
   - In Dataset Settings, go to "Scheduled refresh"
   - Enable "Keep your data up to date"
   - Set refresh frequency: Daily at 6:00 AM
   - Add your email for failure notifications
   - Click "Apply"

---

## Step 4: Implement Row-Level Security

### Define Roles:

1. **In Power BI Desktop**:
   - Go to "Modeling" tab
   - Click "Manage Roles"
   - Create roles:

2. **Department Manager Role**:
   ```dax
   [DepartmentName] = USERPRINCIPALNAME()
   ```
   Apply to: DimDepartment table

3. **Regional Manager Role**:
   ```dax
   [Region] = USERPRINCIPALNAME()
   ```
   Apply to: DimCustomer table

4. **Executive Role**:
   - No filter (see all data)

### Assign Users to Roles (in Power BI Service):

1. Publish the report to Power BI Service
2. Go to the workspace
3. Click "..." next to dataset > "Security"
4. Add users to appropriate roles
5. Click "Save"

---

## Step 5: Publish to Power BI Service

1. **Publish Report**:
   - In Power BI Desktop, click "Publish" button
   - Select destination workspace
   - Wait for publishing to complete

2. **Configure Workspace**:
   - Go to powerbi.microsoft.com
   - Navigate to your workspace
   - Verify report and dataset are present

3. **Test Report**:
   - Open the report in Power BI Service
   - Verify all visuals load correctly
   - Test filters and interactions
   - Check data refresh works

---

## Step 6: Share Dashboard

### Option A: Direct Sharing

1. Open the report in Power BI Service
2. Click "Share" button
3. Enter email addresses of users
4. Optional: Allow recipients to share
5. Optional: Send email notification
6. Click "Grant access"

### Option B: Create Power BI App

1. **Create App**:
   - Go to workspace
   - Click "Create app"
   - Configure app settings:
     - Name: "Executive Dashboard"
     - Description: "Executive dashboard for business insights"
     - App logo: Upload company logo
   - Select content to include
   - Click "Publish app"

2. **Share App**:
   - Copy app link
   - Share link with users
   - Users can install app from link

### Option C: Embed in SharePoint/Teams

1. **Get Embed Code**:
   - Open report in Power BI Service
   - Click "File" > "Embed in SharePoint Online"
   - Copy embed link

2. **Embed in SharePoint**:
   - Create/edit SharePoint page
   - Add "Power BI" web part
   - Paste embed link
   - Save page

---

## Step 7: Maintenance and Monitoring

### Daily Tasks:
- Check data refresh status
- Monitor refresh failures
- Verify data quality

### Weekly Tasks:
- Review dashboard performance
- Check user feedback
- Update documentation if needed

### Monthly Tasks:
- Review and update measures if needed
- Optimize slow-running queries
- Add new features based on user requests

### Monitoring Tools:
- **Power BI Service**: Check refresh history
- **Power BI Premium**: Use metrics app for detailed analysis
- **Gateway Logs**: Monitor gateway performance

---

## Troubleshooting

### Data Refresh Failures:

**Issue**: Refresh fails with "credentials" error
- **Solution**: Update data source credentials in Power BI Service

**Issue**: Refresh fails with "timeout" error
- **Solution**: Optimize queries, add indexes to database, or increase gateway timeout

### Performance Issues:

**Issue**: Visuals load slowly
- **Solution**: 
  - Reduce number of visuals per page
  - Add aggregations
  - Use DirectQuery for large datasets

**Issue**: Dashboard is slow in Power BI Service
- **Solution**:
  - Consider upgrading to Power BI Premium
  - Enable query caching
  - Optimize DAX measures

### Display Issues:

**Issue**: Visuals don't display correctly
- **Solution**:
  - Check data types are correct
  - Verify relationships are properly configured
  - Clear browser cache

---

## Support and Resources

- **Power BI Documentation**: https://docs.microsoft.com/power-bi/
- **Power BI Community**: https://community.powerbi.com/
- **DAX Guide**: https://dax.guide/
- **Internal Support**: Contact your BI team

---

## Appendix

### A. Connection String Examples

**SQL Server**:
```
Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;
```

**Azure SQL Database**:
```
Server=tcp:myserver.database.windows.net,1433;Database=myDataBase;User ID=mylogin@myserver;Password=myPassword;
```

### B. Useful DAX Patterns

**Time Intelligence**:
```dax
-- Previous Month
PM Sales = CALCULATE([Total Sales], PREVIOUSMONTH(DimTime[Date]))

-- Year to Date
YTD Sales = TOTALYTD([Total Sales], DimTime[Date])
```

**Conditional Formatting**:
```dax
-- Status Color
Status Color = 
SWITCH(
    TRUE(),
    [KPI Achievement %] >= 1, "Green",
    [KPI Achievement %] >= 0.9, "Orange",
    "Red"
)
```

### C. Performance Tuning Checklist

- [ ] Remove unused columns from data model
- [ ] Replace calculated columns with measures
- [ ] Use variables in complex DAX expressions
- [ ] Enable query folding for data transformations
- [ ] Add aggregations for large fact tables
- [ ] Set up incremental refresh for historical data
- [ ] Optimize visuals (limit data points)
- [ ] Use summarized tables for common aggregations

