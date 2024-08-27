import pandas as pd
import numpy as np
import json

def read_data(file):
    data_json = {}

    # Read the entire sheet
    df = pd.read_excel(file, sheet_name='Sheet1', header=None)

    # Slice the relevant portion (assuming data starts from B2 and headers are in rows 2 and 3)
    start_row, end_row = 1, 2
    start_col, end_col = 1, 9

    # Extract the headers
    headers = df.iloc[start_row:end_row+1, start_col:end_col+1]
    heads = ['Load_Size', 'Machine Type', 'Finish', 'Fabric', 'Recipe', 'FNO']

    for i in heads:
        mask = headers.eq(i)
        positions = list(zip(*np.where(mask)))

        if (i == 'Finish') or (i == 'Fabric'):
            header_position = headers.eq(i)
            header_positions = list(zip(*np.where(header_position)))
            value = headers.iloc[header_positions[0][0], header_positions[0][1] + 3]
            data_json[i] = value
        else:
            header_position = headers.eq(i)
            header_positions = list(zip(*np.where(header_position)))
            value = headers.iloc[header_positions[0][0], header_positions[0][1] + 1]
            data_json[i] = value

    # Select the data from the DataFrame starting from the 4th row (index 3)
    data = df.iloc[3:,]

    # Extract the column names from the first row of the data
    data_columns = data.iloc[0]

    # Drop the first row of the data (which contains the column names)
    data = data.drop(3).reset_index(drop=True)

    # Set the column names
    data.columns = data.iloc[0]

    # Forward fill relevant columns
    data['LTRs'] = data['LTRs'].ffill(axis=0)
    data['RPM'] = data['RPM'].ffill(axis=0)
    data['Centigrade'] = data['Centigrade'].ffill(axis=0)
    data['ACTION'] = data['ACTION'].ffill(axis=0)
    data['MINS.'] = data['MINS.'].ffill(axis=0)

    # Initialize variables for tracking previous action and step
    prev_action = None
    step = 0

    for index, row in data.iterrows():
        if pd.notnull(row['ACTION']):
            if row['ACTION'] != prev_action:
                step = index + 1
                row = row.fillna('')
                dict_row = row.to_dict()
                dict_row['Chemicals'] = [{'name': row['Chemical Name'], 'Percentage': row['%'], 'Dosage': row['Dosage']}]
                dict_row.pop('Chemical Name')
                dict_row.pop('%')
                dict_row.pop('Dosage')
                data_json[step] = dict_row
                prev_action = row['ACTION']
            else:
                row = row.fillna('')
                data_json[step]['Chemicals'].append({'name': row['Chemical Name'], 'Percentage': row['%'], 'Dosage': row['Dosage']})

    # Print the resulting JSON data
    print(json.dumps(data_json, indent=4))

    # Save the resulting JSON to a file
    with open('recipe-data.json', 'w') as f:
        json.dump(data_json, f, indent=4)

    return data_json


    modifeid_cheimcals = []
    for i in recipe_data.values():
        if type(i) == dict and i['STEP'] != 'STEP':
            processed_step = {
                'step_no': 'None' if i['STEP'] == "STEP" else i['STEP'],
                'action': 'None' if i['ACTION'] == "ACTION" else i['ACTION'],
                'minutes': 0.0 if (i['MINS.'] == "MINS.") or (i['MINS.'] == "None") or (i['ACTION']=='UnLoad') else round(float(i['MINS.']), 1),
                'litres': 0 if (i['LTRs'] == "LTRs") or (i['LTRs'] == "None") or (i['ACTION']=='UnLoad') else i['LTRs'],
                'rpm': 0 if (i['RPM'] == "RPM") or (i['RPM'] == "None") or (i['ACTION']=='UnLoad') else i['RPM'],
                'temperature': 0 if (i['Centigrade'] == "Centigrade") or (i['Centigrade'] == "None") or (i['ACTION']=='UnLoad') else i['Centigrade'],
                'PH': 0 if (i['PH'] == "PH") or (i['PH'] == "None") else i['PH'],
                'TDS': 0 if (i['TDS'] == "TDS") or (i['TDS'] == "None") else i['TDS'],
                'TSS': 0 if (i['TSS'] == "TSS") or (i['TSS'] == "None") else i['TSS'],
                'chemicals': []
            }

            for j in i['Chemicals']:
                if j['name'] != 'None':
                    for k in chemicals:
                        if j['name'] == k['recipe_name']:
                            chemical = k.copy()
                            chemical['percentage'] = round(float(j['%']), 6)
                            chemical['dosage'] = j['Dosage']
                            chemical['kg_per_container'] = int(chemical['kg_per_container'])
                            chemical['cost_per_kg'] = round(float(chemical['cost_per_kg']), 1)
                            if 'isdeleted' in chemical:
                                chemical.pop('isdeleted')
                            if 'created_at' in chemical:
                                chemical.pop('created_at')
                            processed_step['chemicals'].append(chemical)
            modifeid_cheimcals.append(processed_step)


# import pandas as pd
# import numpy as np
# import json
#
#
# def read_data(file):
#     data_json = {}
#
#     # Read the entire sheet
#     df = pd.read_excel(file, sheet_name='Sheet1', header=None)
#
#     # Slice the relevant portion (assuming data starts from B2 and headers are in rows 2 and 3)
#     start_row, end_row = 1, 2
#     start_col, end_col = 1, 9
#
#     # Extract the headers
#     headers = df.iloc[start_row:end_row + 1, start_col:end_col + 1]
#     heads = ['Load_Size', 'Machine Type', 'Finish', 'Fabric', 'Recipe', 'FNO']
#
#     for i in heads:
#         mask = headers.eq(i)
#         positions = list(zip(*np.where(mask)))
#
#         if i in ['Finish', 'Fabric']:
#             header_position = headers.eq(i)
#             header_positions = list(zip(*np.where(header_position)))
#             value = headers.iloc[header_positions[0][0], header_positions[0][1] + 3]
#             data_json[i] = value
#         else:
#             header_position = headers.eq(i)
#             header_positions = list(zip(*np.where(header_position)))
#             value = headers.iloc[header_positions[0][0], header_positions[0][1] + 1]
#             data_json[i] = value
#
#     # Select the data from the DataFrame starting from the 4th row (index 3)
#     data = df.iloc[3:, ]
#
#     # Extract the column names from the first row of the data
#     data_columns = data.iloc[0]
#
#     # Drop the first row of the data (which contains the column names)
#     data = data.drop(3).reset_index(drop=True)
#
#     # Set the column names
#     data.columns = data.iloc[0]
#
#     # Forward fill relevant columns
#     data['LTRs'] = data['LTRs'].ffill(axis=0)
#     data['RPM'] = data['RPM'].ffill(axis=0)
#     data['Centigrade'] = data['Centigrade'].ffill(axis=0)
#     data['ACTION'] = data['ACTION'].ffill(axis=0)
#     data['MINS.'] = data['MINS.'].ffill(axis=0)
#
#     # Initialize variables for tracking previous action and step
#     prev_action = None
#     step = 0
#     modified_chemicals = []
#
#     for index, row in data.iterrows():
#         if pd.notnull(row['ACTION']):
#             if row['ACTION'] != prev_action:
#                 step = index + 1
#                 row = row.fillna('None')
#                 dict_row = row.to_dict()
#                 dict_row['Chemicals'] = [{'name': row['Chemical Name'], '%': row['%'], 'Dosage': row['Dosage']}]
#                 dict_row.pop('Chemical Name')
#                 dict_row.pop('%')
#                 dict_row.pop('Dosage')
#                 data_json[step] = dict_row
#                 prev_action = row['ACTION']
#             else:
#                 row = row.fillna('None')
#                 data_json[step]['Chemicals'].append(
#                     {'name': row['Chemical Name'], '%': row['%'], 'Dosage': row['Dosage']})
#
#     # Process the data to create the modified chemicals data
#     for i in data_json.values():
#         if isinstance(i, dict) and i.get('ACTION') != 'UnLoad':
#             processed_step = {
#                 'step_no': i.get('STEP', 'None'),
#                 'action': i.get('ACTION', 'None'),
#                 'minutes': 0.0 if i.get('MINS.') in ["MINS.", "None"] else round(float(i['MINS.']), 1),
#                 'litres': 0 if i.get('LTRs') in ["LTRs", "None"] else i['LTRs'],
#                 'rpm': 0 if i.get('RPM') in ["RPM", "None"] else i['RPM'],
#                 'temperature': 0 if i.get('Centigrade') in ["Centigrade", "None"] else i['Centigrade'],
#                 'PH': 0 if i.get('PH') in ["PH", "None"] else i['PH'],
#                 'TDS': 0 if i.get('TDS') in ["TDS", "None"] else i['TDS'],
#                 'TSS': 0 if i.get('TSS') in ["TSS", "None"] else i['TSS'],
#                 'chemicals': []
#             }
#
#             for j in i.get('Chemicals', []):
#                 # Safely convert the percentage to a float, defaulting to 0.0 if conversion fails
#                 try:
#                     percentage = round(float(j['%']), 6)
#                 except ValueError:
#                     percentage = 0.0
#
#                 if j['name'] != 'None':
#                     chemical = {
#                         'recipe_name': j['name'],
#                         'percentage': percentage,
#                         'dosage': j['Dosage'],
#                     }
#                     processed_step['chemicals'].append(chemical)
#             modified_chemicals.append(processed_step)
#
#     # Construct the final recipe data
#     recipe = {
#         'load_size': data_json.get('Load_Size', 'None'),
#         'machine_type': data_json.get('Machine Type', 'None'),
#         'finish': data_json.get('Finish', 'None'),
#         'fabric': data_json.get('Fabric', 'None'),
#         'recipe_no': data_json.get('Recipe', 'None'),
#         'Fno': data_json.get('FNO', 'None'),
#         'step': modified_chemicals
#     }
#
#     # Save the resulting JSON to files
#     with open('recipe-data.json', 'w') as f:
#         json.dump(data_json, f, indent=4)
#
#     with open('recipe-data-modified.json', 'w') as f:
#         json.dump(recipe, f, indent=4)
#
#     return recipe

