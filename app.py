from flask import Flask, render_template, request, jsonify
import pdfplumber
import re
import subprocess
import sys
import json
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure app for production
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Mapping of DISCHARGE-LOCATION to OUT-BOUND-Border
BORDER_MAPPING = {
    "KASENYI": "NTOROKO",
    "OMBAY": "LIA",
    "LIA": "LIA",
    "KASINDI": "MPONDWE",
    "GOLI": "GOLI",
    "KAROMBO": "PADEA",
    "VURRA": "VURRA",
    "RUZIZI": "KATUNA",
    "CYANIKA": "CYANIKA"
}

# --- Extraction function for Normal Certificate ---
def extract_normal_certificate_data(extracted_text):
    patterns = {
        "Certificate_No": r"A\.D\s+N°\s+(\S+)",
        "Importer": r"IMPORTATEUR\s*:\s*(.+)",
        "Exporter": r"EXPORTATEUR\s+(.+)",
        "Forwarder": r"TRANSITAIRE\s*:\s*(.+)",
        "Entry_No": r"TITRE DE TRANSPORT\s*:\s*(.+?)\s*TRANS",
        "Final_Destination": r"DEST\. FINALE EN RDC\s*:\s*([A-Z]+)",
        "Discharge_Place": r"LIEU DE\s+([A-Z]+)\s+\d{2}/\d{2}/\d{4}",
        "Transport": r"MOYEN DE TRANSPORT\s*:\s*([\w/ ]+?)\s+VG",
    }

    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        data[key] = match.group(1).strip() if match else None

    # Block-based parse for FOB/Charges
    block_match = re.search(r"VALEUR FOB.*?TOTAL", extracted_text, re.S | re.I)
    if block_match:
        block_text = block_match.group(0)
        numbers = re.findall(r"\d+\.\d+", block_text)
        if len(numbers) >= 4:
            data["FOB_Value"] = numbers[0]
            data["Base_Freight"] = numbers[1]
            data["Additional_Fees"] = numbers[2]
            data["Insurance"] = numbers[3]
            data["transporterName"] = "OWN"
            data["validationNotes"] = "please verify"

    # Extract Goods Descriptions
    descriptions_list = []
    start_marker = r"MARCHANDISE\s+N\.C\.\s+Pays\s*:"
    end_marker = r"TYPE NR COLIS"
    
    start_matches = list(re.finditer(start_marker, extracted_text, re.IGNORECASE))
    end_match = re.search(end_marker, extracted_text, re.IGNORECASE)
    
    if start_matches and end_match:
        for i, start_match in enumerate(start_matches):
            start_pos = start_match.end()
            if i < len(start_matches) - 1:
                end_pos = start_matches[i + 1].start()
            else:
                end_pos = end_match.start()
            
            goods_text = extracted_text[start_pos:end_pos].strip()
            
            description_match = re.search(
                r"[A-Z]+\s*HS\s*:\s*([^\n]*)\n([\s\S]*?)(?=(?:\s*MARCHANDISE\s+N\.C\.\s+Pays\s*:|\s*VALEURS DECLAREES PAR L'EXPORTATEUR|$))",
                goods_text,
                re.IGNORECASE
            )
            if description_match:
                description = description_match.group(2)
                description = ' '.join(description.split()).strip()
                descriptions_list.append(description)
    
    data["Descriptions"] = descriptions_list if descriptions_list else ["No descriptions extracted"]

    return data

# --- Extraction function for AD Certificate ---
def extract_ad_certificate_data(extracted_text):
    patterns = {
        "Certificate_No": r"AD\s*N°\s*:?([0-9A-Z/ ]+)",
        "Importer": r"IMPORTATEUR\s*:?\s*([^\n]+?)(?=\s*BL#:|$)",
        "Transporteur": r"(?<!ID\s)Transporteur\s*:\s*(.+?)(?=\s+Fret\b|$)",
        "Carrier": r"Carrier:\s*([^\n]+)(?=\s+On\b|$)",
        "Forwarder": r"Transitaire:\s*([^\n]+)",
        "Entry_No": r"N°\s*Declaration\s*([\w\d]+(?:\s[\w\d]+)*)(?=\s*Agent)",
        "Discharge_Place": r"Lieu d'entrée en RDC:?\s*([A-Z]+)",
        "Final_Destination": r"Destination finale en\s*([A-Z][A-Za-z]*)\b",
        "Transport": r"ID Transporteur:?\s*([^\n]+)",
        "Descriptions": r"MARCHANDISE\s*:\s*([^\n]+)",
        "FOB_Value": r"Valeur FOB\s*:\s*([\d.,]+)",
        "Base_Freight": r"Valeur Fret\s*:\s*([\d.,]+)",
        "Insurance": r"Assurance\s*([\d.,]+)\s*USD"
    }

    data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, extracted_text, re.IGNORECASE)
        if match:
            try:
                data[key] = match.group(1).strip()
            except IndexError:
                data[key] = match.group(0).strip()
        else:
            data[key] = None

    # --- New Exporter field ---
    transporteur = data.get("Transporteur") or ""
    carrier = data.get("Carrier") or ""
    exporter = f"{transporteur} {carrier}".strip() if (transporteur or carrier) else None
    data["Exporter"] = exporter

    # Keep your custom extra fields
    data["transporterName"] = "OWN"
    data["validationNotes"] = "please verify"

    return data

# --- Main extraction function ---
def extract_certificate_data(pdf_file):
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    # Determine certificate type based on content
    if re.search(r"AD\s*N°", extracted_text, re.IGNORECASE):
        data = extract_ad_certificate_data(extracted_text)
        data["Certificate_Type"] = "AD"
    else:
        data = extract_normal_certificate_data(extracted_text)
        data["Certificate_Type"] = "Normal"

    # Map Discharge_Place to OUT-BOUND-Border
    discharge_place = data.get("Discharge_Place")
    data["Out_Bound_Border"] = BORDER_MAPPING.get(discharge_place, "UNKNOWN") if discharge_place else "UNKNOWN"

    return data

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = None
    if request.method == "POST":
        try:
            if "pdf" not in request.files:
                logger.warning("No PDF file in request")
                return "No file uploaded", 400
            
            pdf_file = request.files["pdf"]
            if pdf_file.filename == "":
                logger.warning("No file selected")
                return "No selected file", 400
            
            if not pdf_file.filename.lower().endswith('.pdf'):
                logger.warning(f"Invalid file type: {pdf_file.filename}")
                return "Please upload a PDF file", 400

            logger.info(f"Processing PDF file: {pdf_file.filename}")
            extracted_data = extract_certificate_data(pdf_file)
            logger.info("PDF processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            return f"Error processing PDF: {str(e)}", 500

    return render_template("index.html", data=extracted_data)

@app.route("/open-form", methods=["POST"])
def open_form():
    """Open the Invesco form in the user's browser with instructions"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Return the form URL and instructions for client-side handling
        form_url = "https://www.invesco-ug.com/business/application/new"
        
        # Generate form settings based on certificate type
        cert_type = data.get('Certificate_Type', 'Normal')
        form_settings = {
            "issuing_body": "DR CONGO",
            "cert_type": "CONTINUANCE" if cert_type == "AD" else "REGIONAL",
            "cargo_origin": "OUTSIDE UGANDA" if cert_type == "AD" else "UGANDA",
            "shipment_route": "OUT-BOUND",
            "transport_mode": "ROAD",
            "fob_currency": "USD",
            "freight_currency": "USD",
            "out_bound_border": data.get('Out_Bound_Border', 'UNKNOWN')
        }
        
        return jsonify({
            "status": "success",
            "form_url": form_url,
            "form_settings": form_settings,
            "extracted_data": data
        })
    except Exception as e:
        logger.error(f"Error in open_form: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({"status": "healthy", "service": "invesco-pdf-extractor"})

# --- Run the app ---
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)