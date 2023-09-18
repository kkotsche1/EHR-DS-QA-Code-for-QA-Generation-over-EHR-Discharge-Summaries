import json
import csv

# Step 1: Load the JSON data
with open('../ehr_notes_qa_final.json') as f:
    data = json.load(f)

# Step 2: Identify the fields (assuming that the JSON data is a list of dictionaries)
fields = list(data[0].keys())

# Step 3: Write data to a CSV file
with open('../ehr_notes_qa_final.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Write the header
    writer.writerow(fields)

    # Write the data rows
    for row in data:
        writer.writerow([row.get(field, '') for field in fields])
