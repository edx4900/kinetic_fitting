import pandas as pd
import os
import re


def load_data(directory_path, experiment_type, substrate):
    # Getting all excel files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx') and not f.startswith('~$')]

    data = {}
    for f in files:
        # Load excel file
        print(f"Processing file: {f}")  # Add this line
        xls = pd.ExcelFile(os.path.join(directory_path, f), engine='openpyxl')

        for sheet_name in xls.sheet_names:
            if experiment_type == "pH" or experiment_type == "temp":
                # Extract value
                key = float(re.findall(r"[-+]?\d*\.\d+|\d+", sheet_name)[0])
            elif experiment_type == "sKIE":
                # Use sheet name as key
                key = sheet_name
            elif experiment_type == "sub":
                key = f'{substrate}'
            else:
                continue

            # Read the sheet as a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name)

            # Create nested dict if not already existing
            if key not in data:
                data[key] = {}

            # Convert all column names in df to lowercase
            df.columns = df.columns.str.lower()

            # Add data under nested key = file name
            data[key][f] = df[['concentration', 'rate']]

    return data
