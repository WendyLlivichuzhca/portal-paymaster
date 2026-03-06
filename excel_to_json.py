import pandas as pd
import json
import sys

def excel_to_json(excel_file, json_file):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)

        # Replace NaN with None (null in JSON)
        df = df.where(pd.notna(df), None)
        
        # Convert to list of dictionaries
        data = df.to_dict('records')

        # Write to JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Successfully converted {excel_file} to {json_file}")
        print(f"Processed {len(data)} records")

    except Exception as e:
        print(f"Error converting Excel to JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python excel_to_json.py <excel_file>")
        sys.exit(1)

    excel_file = sys.argv[1]
    json_file = 'data.json'

    excel_to_json(excel_file, json_file)