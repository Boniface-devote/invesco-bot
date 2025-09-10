import math

def insert_data(ws, data, freight_number, container_type='', num_containers=1, template_file=None):
    """
    Insert extracted data into the Excel worksheet for 'normal' PDF type.
    """
    if 'attestation_number' in data:
        ws['E6'] = f"FERI/AD: {data['attestation_number']}"
        ws['B11'] = f"CERTIFICATE (FERI/ADR/AD) No : {data['attestation_number']}"
    
    if 'forwarding_agent' in data:
        ws['B8'] = f"DEBTOR: {data['forwarding_agent']}"
    
    if 'importateur' in data:
        ws['B10'] = f"IMPORTER: {data['importateur']}"
    
    if 'transport_id' in data:
        ws['B14'] = data['transport_id']
    
    if freight_number is not None:
        ws['D18'] = freight_number

    # Handle CBM field
    if 'cbm' in data:
        try:
            cbm_value = float(data['cbm'])  # already extracted as float from regex
            specific_templates = ['Corporate Legends Limited.xlsx', 'RHO LOGISTICS AND FREIGHT FORWARDER.xlsx']
            
            if template_file in specific_templates:
                truncated_cbm = math.trunc(cbm_value)
                ws['D14'] = truncated_cbm
            
            else:
                ft_20_templates = ['PROFORMA_INVOICE_1x20.xlsx']
                if template_file in ft_20_templates:
                    ws['D14'] = 60
                else:
                    ws['D14'] = cbm_value
        except (ValueError, TypeError):
            # fallback if cbm format is wrong
            ws['D14'] = data['cbm']
