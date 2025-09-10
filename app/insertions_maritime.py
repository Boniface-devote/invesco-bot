def insert_data(ws, data, freight_number, container_type, num_containers, template_file=None):
    """
    Insert extracted data into the Excel worksheet for 'maritime' PDF type.
    """
    if 'feri_number' in data:
        ws['E6'] = f"FERI/AD: {data['feri_number']}"
        ws['B11'] = f"CERTIFICATE (FERI/ADR/AD) No : {data['feri_number']}"
        
    elif 'attestation_number' in data:
        ws['E6'] = f"FERI/AD: {data['attestation_number']}"
        ws['B11'] = f"CERTIFICATE (FERI/ADR/AD) No : {data['attestation_number']}"
    
    if 'transitaire' in data:
        ws['B8'] = f"DEBTOR: {data['transitaire']}"
    
    if 'importateur' in data:
        ws['B10'] = f"IMPORTER: {data['importateur']}"
    
    if 'bl' in data:
        ws['B14'] = data['bl']
    
    # Handle CBM based on template and container type
    specific_templates = ['Proforma_Invoice malaba cement 0.5.xlsx', 
                          'Proforma_Invoice malaba.xlsx',
                          'Proforma_roro.xlsx']
    if template_file in specific_templates and 'cbm' in data:
        cbm_value = float(data['cbm'])  # already a float from extraction
        ws['D14'] = cbm_value
    else:
        if container_type == '40FT':
            ws['D14'] = 110
            ws['E14'] = num_containers
            ws['D17'] = num_containers
            # Handle freight number (overrides default calculation if provided)
            if freight_number is not None:
                ws['D18'] = freight_number
            else:
                ws['D18'] = num_containers * 250
        elif container_type == '20FT':
            ws['D14'] = 60
            ws['E14'] = num_containers
            ws['D17'] = num_containers
            # Handle freight number (overrides default calculation if provided)
            if freight_number is not None:
                ws['D18'] = freight_number
            else:
                ws['D18'] = num_containers * 250
        
        
        # # Insert number of containers for non-specific templates