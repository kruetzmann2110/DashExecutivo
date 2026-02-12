# Quick Start Guide - Executive Dashboard

## For Business Users

### Accessing the Dashboard:

1. **Via Power BI Service**:
   - Go to https://app.powerbi.com
   - Sign in with your work account
   - Navigate to "Workspaces" > "Executive Dashboard"
   - Click on the report to open

2. **Via Power BI App**:
   - Install the "Executive Dashboard" app from your email invitation
   - Open the app from Power BI mobile or web

### Using the Dashboard:

#### Navigation:
- **Pages**: Use tabs at the bottom to switch between dashboard pages
- **Home**: Click the dashboard icon to return to Executive Overview

#### Filtering Data:
- **Date Range**: Use the date slicer to select time period
- **Department**: Filter by specific departments
- **Region**: Filter by geographic region
- **Category**: Filter by product categories

#### Interactive Features:
- **Click on visuals**: Click on bars, pie slices, or data points to cross-filter
- **Drill-through**: Right-click on data points and select "Drill through" for details
- **Tooltips**: Hover over visuals to see additional information
- **Export**: Click "..." on any visual to export data to Excel

#### Key Metrics:

**Executive Overview**:
- Monitor overall business performance
- Track sales trends vs last year
- Identify top performing departments and products

**Financial Performance**:
- Track budget vs actual performance
- Monitor profit margins
- View financial KPIs by department

**Sales Analysis**:
- Analyze sales by category and segment
- Identify sales trends
- Review product performance

**Customer Insights**:
- Track customer metrics and retention
- Identify top customers
- Analyze customer distribution

**KPI Dashboard**:
- Monitor key performance indicators
- Track achievement vs targets
- View KPI trends over time

---

## For IT/Admin Users

### Initial Setup:

1. **Clone Repository**:
   ```bash
   git clone https://github.com/kruetzmann2110/DashExecutivo.git
   cd DashExecutivo
   ```

2. **Setup Database**:
   ```bash
   # Execute the schema
   sqlcmd -S your_server -d your_database -i DataModel/schema.sql
   ```

3. **Generate Test Data** (optional):
   ```bash
   cd SampleData
   python generate_sample_data.py
   # Import generated CSV files to database
   ```

4. **Create Power BI Report**:
   - Open Power BI Desktop
   - File > New
   - Get Data > SQL Server (or your data source)
   - Load all dimension and fact tables
   - Go to Model view and create relationships:
     - Connect all fact tables to dimension tables via their keys
     - Set cardinality to Many-to-One
   - Copy measures from `DAX/measures.dax` and create them in a "Measures" table
   - Build pages following `Documentation/dashboard_design.md`

5. **Publish**:
   - Click "Publish" in Power BI Desktop
   - Select workspace
   - Configure refresh schedule
   - Set up RLS roles
   - Share with users

### Maintenance:

- **Daily**: Monitor data refresh status
- **Weekly**: Review performance and user feedback
- **Monthly**: Update measures and optimize queries

---

## For Developers

### Development Environment:

1. **Tools Required**:
   - Power BI Desktop (latest)
   - Python 3.x
   - SQL Server Management Studio (or Azure Data Studio)
   - Git

2. **Project Structure**:
   ```
   DashExecutivo/
   ├── DataModel/        # Database schemas
   ├── DAX/             # DAX measures
   ├── SampleData/      # Sample data generation
   ├── Documentation/   # Detailed docs
   └── Configuration/   # Config templates
   ```

3. **Making Changes**:
   - Create a feature branch
   - Make changes to relevant files
   - Test changes in Power BI Desktop
   - Update documentation
   - Create pull request

4. **Adding New Measures**:
   - Add DAX code to `DAX/measures.dax`
   - Document the measure purpose
   - Test thoroughly
   - Update dashboard pages as needed

5. **Modifying Data Model**:
   - Update `DataModel/schema.sql`
   - Update sample data generator if needed
   - Document changes in deployment guide
   - Update relationships in Power BI

---

## Troubleshooting

### Common Issues:

**Can't see the dashboard**:
- Check you have correct permissions
- Verify you're logged into Power BI with work account
- Contact your admin for access

**Data looks incorrect**:
- Check filters are not limiting your view
- Verify date range is set correctly
- Clear all filters and try again

**Refresh failed**:
- Check network connectivity
- Verify database credentials
- Check gateway status (for on-premises data)

**Slow performance**:
- Reduce date range filter
- Clear browser cache
- Contact admin if issue persists

---

## Support

- **Email**: support@yourdomain.com
- **Documentation**: See /Documentation folder
- **Issues**: Report on GitHub Issues

---

## Training Resources

- **Video Tutorials**: [Link to training videos]
- **User Manual**: See full documentation
- **Power BI Basics**: https://docs.microsoft.com/power-bi/

---

**Last Updated**: 2024-01-01
