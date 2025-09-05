#!/usr/bin/env python3
"""
Client-side browser automation script
This script runs on the user's local machine to fill forms
"""

import webbrowser
import json
import sys
import os
from urllib.parse import urlencode

def open_browser_with_data(extracted_data):
    """
    Open the user's browser with pre-filled form data
    """
    try:
        # Create a temporary HTML file with the form data
        html_content = create_form_html(extracted_data)
        
        # Write to a temporary file
        temp_file = "temp_form.html"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Get the absolute path
        file_path = os.path.abspath(temp_file)
        file_url = f"file:///{file_path.replace(os.sep, '/')}"
        
        # Open in the default browser
        webbrowser.open(file_url)
        
        print("Browser opened with form data. Please complete the form submission manually.")
        print(f"Form data file: {file_path}")
        
        return True
        
    except Exception as e:
        print(f"Error opening browser: {str(e)}")
        return False

def create_form_html(data):
    """
    Create an HTML page with the form pre-filled with extracted data
    """
    # Map the extracted data to form field values
    form_data = {
        'certificateNumber': data.get('Certificate_No', ''),
        'customsDeclarationNumber': data.get('Entry_No', ''),
        'importerName': data.get('Importer', ''),
        'exporterName': data.get('Exporter', ''),
        'importAgentName': data.get('Forwarder', ''),
        'exportAgentName': data.get('Forwarder', ''),
        'transporterName': data.get('transporterName', 'OWN'),
        'vehicleNumber': data.get('Transport', ''),
        'dischargeLocation': data.get('Discharge_Place', ''),
        'finalDestination': data.get('Final_Destination', ''),
        'fobValue': data.get('FOB_Value', ''),
        'freightValue': data.get('Base_Freight', ''),
        'validationNotes': data.get('validationNotes', 'please verify'),
        'cargoDescription': '\\n'.join(data.get('Descriptions', [])) if data.get('Descriptions') else ''
    }
    
    # Determine certificate type settings
    cert_type = data.get('Certificate_Type', 'Normal')
    issuing_body = 'DR CONGO'
    cert_type_value = 'CONTINUANCE' if cert_type == 'AD' else 'REGIONAL'
    cargo_origin = 'OUTSIDE UGANDA' if cert_type == 'AD' else 'UGANDA'
    shipment_route = 'OUT-BOUND'
    transport_mode = 'ROAD'
    fob_currency = 'USD'
    freight_currency = 'USD'
    out_bound_border = data.get('Out_Bound_Border', 'UNKNOWN')
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invesco Form - Pre-filled Data</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #007bff;
        }}
        .form-section {{
            margin-bottom: 25px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }}
        .form-section h3 {{
            color: #007bff;
            margin-top: 0;
        }}
        .form-group {{
            margin-bottom: 15px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }}
        input, textarea, select {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }}
        textarea {{
            height: 80px;
            resize: vertical;
        }}
        .instructions {{
            background-color: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .instructions h4 {{
            color: #0066cc;
            margin-top: 0;
        }}
        .data-display {{
            background-color: #f0f8f0;
            border: 1px solid #90ee90;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .data-display h4 {{
            color: #006600;
            margin-top: 0;
        }}
        .data-item {{
            margin-bottom: 8px;
        }}
        .data-label {{
            font-weight: bold;
            color: #333;
        }}
        .data-value {{
            color: #666;
            margin-left: 10px;
        }}
        .button-group {{
            text-align: center;
            margin-top: 30px;
        }}
        .btn {{
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 0 10px;
            text-decoration: none;
            display: inline-block;
        }}
        .btn:hover {{
            background-color: #0056b3;
        }}
        .btn-success {{
            background-color: #28a745;
        }}
        .btn-success:hover {{
            background-color: #1e7e34;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Invesco Form - Pre-filled with Extracted Data</h1>
            <p>Certificate Type: {cert_type} | Border: {out_bound_border}</p>
        </div>
        
        <div class="instructions">
            <h4>📋 Instructions:</h4>
            <ol>
                <li>Review the extracted data below</li>
                <li>Click "Open Invesco Form" to go to the actual form</li>
                <li>Copy and paste the values from this page to the form</li>
                <li>Complete any remaining fields and submit</li>
            </ol>
        </div>
        
        <div class="data-display">
            <h4>📊 Extracted Data:</h4>
            <div class="data-item">
                <span class="data-label">Certificate Number:</span>
                <span class="data-value">{form_data['certificateNumber']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Entry Number:</span>
                <span class="data-value">{form_data['customsDeclarationNumber']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Importer:</span>
                <span class="data-value">{form_data['importerName']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Exporter:</span>
                <span class="data-value">{form_data['exporterName']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Forwarder:</span>
                <span class="data-value">{form_data['importAgentName']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Transporter:</span>
                <span class="data-value">{form_data['transporterName']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Vehicle Number:</span>
                <span class="data-value">{form_data['vehicleNumber']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Discharge Location:</span>
                <span class="data-value">{form_data['dischargeLocation']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Final Destination:</span>
                <span class="data-value">{form_data['finalDestination']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">FOB Value:</span>
                <span class="data-value">{form_data['fobValue']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Freight Value:</span>
                <span class="data-value">{form_data['freightValue']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Validation Notes:</span>
                <span class="data-value">{form_data['validationNotes']}</span>
            </div>
            <div class="data-item">
                <span class="data-label">Cargo Description:</span>
                <span class="data-value">{form_data['cargoDescription']}</span>
            </div>
        </div>
        
        <div class="form-section">
            <h3>Form Settings (for reference):</h3>
            <div class="form-group">
                <label>Issuing Body:</label>
                <input type="text" value="{issuing_body}" readonly>
            </div>
            <div class="form-group">
                <label>Cert. Type:</label>
                <input type="text" value="{cert_type_value}" readonly>
            </div>
            <div class="form-group">
                <label>Cargo Origin:</label>
                <input type="text" value="{cargo_origin}" readonly>
            </div>
            <div class="form-group">
                <label>Shipment Route:</label>
                <input type="text" value="{shipment_route}" readonly>
            </div>
            <div class="form-group">
                <label>Transport Mode:</label>
                <input type="text" value="{transport_mode}" readonly>
            </div>
            <div class="form-group">
                <label>FOB Currency:</label>
                <input type="text" value="{fob_currency}" readonly>
            </div>
            <div class="form-group">
                <label>Freight Currency:</label>
                <input type="text" value="{freight_currency}" readonly>
            </div>
            <div class="form-group">
                <label>Out-Bound Border:</label>
                <input type="text" value="{out_bound_border}" readonly>
            </div>
        </div>
        
        <div class="button-group">
            <a href="https://www.invesco-ug.com/business/application/new" target="_blank" class="btn btn-success">
                🚀 Open Invesco Form
            </a>
            <button onclick="copyAllData()" class="btn">
                📋 Copy All Data
            </button>
            <button onclick="downloadData()" class="btn">
                💾 Download Data
            </button>
        </div>
    </div>
    
    <script>
        function copyAllData() {{
            const data = `{json.dumps(form_data, indent=2)}`;
            navigator.clipboard.writeText(data).then(() => {{
                alert('Data copied to clipboard!');
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = data;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('Data copied to clipboard!');
            }});
        }}
        
        function downloadData() {{
            const data = `{json.dumps(form_data, indent=2)}`;
            const blob = new Blob([data], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'invesco_form_data.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
    </script>
</body>
</html>
"""
    return html_template

if __name__ == "__main__":
    # Read data from command line argument or stdin
    if len(sys.argv) > 1:
        data_str = sys.argv[1]
    else:
        data_str = sys.stdin.read()
    
    try:
        extracted_data = json.loads(data_str)
        success = open_browser_with_data(extracted_data)
        if success:
            print("SUCCESS: Browser opened with form data")
        else:
            print("ERROR: Failed to open browser")
            sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
