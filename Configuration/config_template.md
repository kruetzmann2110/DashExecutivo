# Power BI Template Configuration

## Data Source Configuration

### Connection String Template:
```
Server=YOUR_SERVER_NAME;Database=YOUR_DATABASE_NAME;User Id=YOUR_USERNAME;Password=YOUR_PASSWORD;
```

### For Azure SQL Database:
```
Server=tcp:YOUR_SERVER.database.windows.net,1433;Database=YOUR_DATABASE;User ID=YOUR_LOGIN@YOUR_SERVER;Password=YOUR_PASSWORD;Encrypt=yes;TrustServerCertificate=no;
```

---

## Refresh Schedule Configuration

- **Refresh Time**: 06:00 AM (local time)
- **Frequency**: Daily
- **Time Zone**: UTC
- **Email Notifications**: Enabled on failure

---

## Performance Settings

### Query Timeout:
- **Default**: 600 seconds (10 minutes)
- **For large datasets**: 1800 seconds (30 minutes)

### Maximum Rows:
- **Development**: 1,000,000 rows
- **Production**: Unlimited (with aggregations)

---

## Security Configuration

### Row-Level Security Roles:

1. **Department_Manager**:
   - Filter: `DimDepartment[ManagerName] = USERPRINCIPALNAME()`

2. **Regional_Manager**:
   - Filter: `DimCustomer[Region] = USERNAME()`

3. **Executive**:
   - Filter: None (full access)

---

## Workspace Settings

### Workspace Name:
- Development: `Executive_Dashboard_Dev`
- Testing: `Executive_Dashboard_Test`
- Production: `Executive_Dashboard_Prod`

### Capacity:
- **License Type**: Power BI Pro / Premium
- **Recommended Capacity**: P1 or higher for large datasets

---

## Email Configuration

### Alert Recipients:
```
admin@yourdomain.com
bi-team@yourdomain.com
```

### Notification Types:
- Data refresh failures
- Performance degradation
- Security alerts

---

## Custom Branding

### Logo Placement:
- **Size**: 200x80 pixels
- **Format**: PNG with transparent background
- **Location**: Top-left corner of each page

### Company Colors:
Replace the default colors with your company's brand colors in:
- `Documentation/dashboard_design.md`
- Theme JSON file (if using custom theme)

---

## Feature Flags

### Enabled Features:
- [x] Cross-filtering
- [x] Drill-through
- [x] Tooltips
- [x] Mobile layout
- [x] Export to Excel
- [x] Export to PDF

### Disabled Features:
- [ ] Print preview
- [ ] Public embedding

---

## Deployment Checklist

- [ ] Database schema created
- [ ] Sample data generated (for testing)
- [ ] Data source configured
- [ ] Relationships established
- [ ] DAX measures added
- [ ] Visuals created per specifications
- [ ] Slicers and filters configured
- [ ] RLS roles defined
- [ ] Published to Power BI Service
- [ ] Data refresh scheduled
- [ ] Users assigned to roles
- [ ] Dashboard shared with stakeholders
- [ ] Documentation updated
- [ ] Training completed

---

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| YYYY-MM-DD | 1.0 | Initial release | Your Name |

---

## Notes

- Remember to update connection strings before publishing
- Test RLS before deploying to production
- Always backup .pbix files before major changes
- Keep DAX measures documented
- Monitor refresh failures daily
