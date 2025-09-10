def insert_data(ws, data, freight_number, container_type, num_containers, template_file=None):
    """
    Insert extracted data into the Excel worksheet for 'possiano' PDF type.
    Mirrors maritime logic but uses different defaults where needed.
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
    if container_type == '40FT':
        ws['D14'] = 110
        ws['E14'] = num_containers
        ws['D17'] = num_containers
    elif container_type == '20FT':
        ws['D14'] = 60
        ws['E14'] = num_containers
        ws['D17'] = num_containers
    elif 'cbm' in data:
        try:
            cbm_value = float(str(data['cbm']).replace(' CBM', ''))
            ws['D14'] = cbm_value
        except Exception:
            pass

    # Freight number; default multiplier for Possiano is 200 per container
    if freight_number is not None:
        ws['D18'] = freight_number
    else:
        ws['D18'] = num_containers * 200


