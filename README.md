# Invesco PDF Certificate Extractor

A Flask web application that extracts data from PDF certificates and can automatically fill forms on the Invesco website.

## Features

- **PDF Data Extraction**: Extracts data from both Normal and AD certificates
- **Form Auto-filling**: Automatically fills forms on the Invesco website (local only)
- **Cloud Deployment**: Ready for deployment on Railway
- **Data Export**: Download extracted data as JSON

## Local Development

### Prerequisites

- Python 3.11+
- Edge WebDriver (for form filling functionality)

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment variables:
   ```bash
   cp env.example .env
   ```

5. Edit `.env` file with your credentials:
   ```
   EMAIL_ADDRESS=your-email@example.com
   PASSWORD=your-password
   ```

6. Run the application:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Railway Deployment

### Prerequisites

- Railway account
- GitHub repository with your code

### Deployment Steps

1. **Connect to Railway**:
   - Go to [Railway Dashboard](https://railway.com/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Environment Variables**:
   In Railway dashboard, go to your project → Variables tab and add:
   ```
   RAILWAY_ENVIRONMENT=production
   FLASK_ENV=production
   EMAIL_ADDRESS=your-email@example.com
   PASSWORD=your-password
   LOGIN_URL=https://www.invesco-ug.com/auth/login
   TARGET_URL=https://www.invesco-ug.com/business/application/new
   ```

3. **Deploy**:
   - Railway will automatically detect the Python application
   - The deployment will use the `Procfile` and `requirements.txt`
   - Your app will be available at the provided Railway URL

### Important Notes for Railway

- **Form Filling Limitation**: Due to browser automation limitations in cloud environments, the form filling feature is disabled on Railway
- **Data Extraction**: PDF data extraction works perfectly on Railway
- **Manual Process**: Users can download the extracted data as JSON and fill forms manually

## Usage

1. **Upload PDF**: Select a certificate PDF file
2. **Extract Data**: Click "Extract" to process the PDF
3. **View Results**: Review the extracted data in the table
4. **Fill Form**: 
   - **Local**: Click "Fill Form" for automatic form filling
   - **Railway**: Download data as JSON and fill manually
5. **Download Data**: Click "Download Data as JSON" to save extracted data

## Supported Certificate Types

- **Normal Certificates**: Standard import/export certificates
- **AD Certificates**: Special AD type certificates

## File Structure

```
├── app.py                 # Main Flask application
├── login.py              # Selenium automation script
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── Procfile             # Railway deployment config
├── runtime.txt          # Python version specification
├── railway.json         # Railway-specific configuration
├── env.example          # Environment variables template
└── README.md            # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RAILWAY_ENVIRONMENT` | Set to 'production' for Railway | - |
| `FLASK_ENV` | Flask environment | 'production' |
| `PORT` | Port number | 5000 |
| `EMAIL_ADDRESS` | Invesco login email | - |
| `PASSWORD` | Invesco login password | - |
| `LOGIN_URL` | Invesco login URL | Default URL |
| `TARGET_URL` | Invesco form URL | Default URL |

## Troubleshooting

### Local Development
- Ensure Edge WebDriver is in the project directory
- Check that all environment variables are set correctly
- Verify PDF files are valid and readable

### Railway Deployment
- Check Railway logs for any errors
- Ensure all required environment variables are set
- Verify the application starts successfully

## Security Notes

- Never commit credentials to version control
- Use environment variables for sensitive data
- Consider using Railway's secret management for production

## Support

For issues or questions, please check the logs and ensure all dependencies are properly installed.
