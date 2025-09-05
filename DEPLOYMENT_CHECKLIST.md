# Railway Deployment Checklist

## Pre-Deployment

- [ ] All files committed to Git repository
- [ ] Environment variables configured in Railway dashboard
- [ ] Railway account connected to GitHub repository

## Required Environment Variables in Railway

Set these in Railway Dashboard → Your Project → Variables:

```
RAILWAY_ENVIRONMENT=production
FLASK_ENV=production
EMAIL_ADDRESS=your-email@example.com
PASSWORD=your-password
LOGIN_URL=https://www.invesco-ug.com/auth/login
TARGET_URL=https://www.invesco-ug.com/business/application/new
```

## Files Required for Deployment

- [x] `app.py` - Main Flask application
- [x] `login.py` - Selenium automation (disabled in cloud)
- [x] `templates/index.html` - Web interface
- [x] `requirements.txt` - Python dependencies
- [x] `Procfile` - Railway startup command
- [x] `runtime.txt` - Python version
- [x] `railway.json` - Railway configuration
- [x] `README.md` - Documentation

## Post-Deployment Verification

- [ ] Application starts successfully
- [ ] Health check endpoint responds: `/health`
- [ ] PDF upload and extraction works
- [ ] Data display in table works
- [ ] JSON download functionality works
- [ ] Form filling shows appropriate message for cloud environment

## Testing Steps

1. **Basic Functionality**:
   - Visit your Railway URL
   - Upload a test PDF certificate
   - Verify data extraction works
   - Check data display in table

2. **Data Export**:
   - Click "Download Data as JSON"
   - Verify JSON file downloads correctly

3. **Form Filling**:
   - Click "Fill Form with Extracted Data"
   - Should show message about cloud limitations
   - Should provide option to download data manually

## Troubleshooting

If deployment fails:
1. Check Railway logs for errors
2. Verify all environment variables are set
3. Ensure Python version compatibility
4. Check that all dependencies are in requirements.txt

## Security Reminders

- Never commit `.env` file with real credentials
- Use Railway's secret management for production
- Regularly rotate passwords and API keys
