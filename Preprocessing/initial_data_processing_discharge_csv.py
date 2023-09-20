import csv
import sqlite3
from tqdm import tqdm

# Your CSV file and database name
file_name = "../csv_files/discharge.csv"
DATABASE_NAME = "EHR_discharge_notes_metadata.db"

def initialize_db(database_name="EHR_discharge_notes_metadata.db"):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discharge_notes (
            id INTEGER PRIMARY KEY,
            note TEXT NOT NULL,
            note_id TEXT,
            subject_id TEXT,
            hadm_id TEXT,
            note_type TEXT,
            note_seq TEXT,
            charttime TEXT,
            storetime TEXT
        )
    """)

    conn.commit()
    conn.close()

def split_records(text):
    # Split based on 'Name: ' but without keeping the delimiter
    records = [record.strip() for record in text.split('Name: ') if record and record != 'Name:']
    # Prepending "Name: " to each record except for the ones that are just "Name:"
    return ["Name: " + record for record in records if record]


def insert_discharge_note(note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, storetime):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO discharge_notes 
        (note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, storetime) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, storetime))

    conn.commit()
    conn.close()

initialize_db(DATABASE_NAME)
with open(file_name, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for row in tqdm(csv_reader):
        individual_records = split_records(row['text'])
        for record in individual_records:
            # You would need to adjust this line to extract the new fields from each record
            insert_discharge_note(record, row['note_id'], row['subject_id'], row['hadm_id'], row['note_type'],
                                  row['note_seq'], row['charttime'], row['storetime'])