from flask import Flask, render_template, request, jsonify
import pdfplumber
import re
import subprocess
import sys
import json

app = Flask(__name__)

# Mapping of DISCHARGE-LOCATION to OUT-BOUND-Border
BORDER_MAPPING = {
    "KASENYI": "NTOROKO",
    "OMBAY": "LIA",
    "KASINDI": "MPONDWE",
    "GOLI": "GOLI",
    "KAROMBO": "PADEA",
    "VURRA": "VURRA",
    "RUZIZI": "KATUNA",
    "CYANIKA": "CYANIKA"
}

# --- Extraction function ---
def extract_certificate_data(pdf_file):
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:   # open directly from file-like object
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"

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

    # Map Discharge_Place to OUT-BOUND-Border
    discharge_place = data.get("Discharge_Place")
    data["Out_Bound_Border"] = BORDER_MAPPING.get(discharge_place, "UNKNOWN") if discharge_place else "UNKNOWN"

    return data

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = None
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file uploaded", 400
        pdf_file = request.files["pdf"]
        if pdf_file.filename == "":
            return "No selected file", 400

        extracted_data = extract_certificate_data(pdf_file)  # pass directly

    return render_template("index.html", data=extracted_data)

@app.route("/fill-form", methods=["POST"])
def fill_form():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        result = subprocess.run(
            [sys.executable, "login.py"],
            input=json.dumps(data),
            text=True,
            capture_output=True
        )
        return jsonify({"status": "success", "output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Run the app ---
if __name__ == "__main__":
    app.run(debug=True)
