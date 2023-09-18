import csv
import sqlite3
from tqdm import tqdm

# Specify the path to your CSV file and the name of your SQLite database
file_name = "../csv_files/discharge.csv"
DATABASE_NAME = "EHR_discharge_notes_metadata.db"


def initialize_db(database_name="EHR_discharge_notes_metadata.db"):
    """
    Initialize the SQLite database with a table structure to store discharge notes metadata.

    Args:
        database_name (str): The name of the database file to create or connect to.
    """
    # Establish a connection to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(database_name)
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a SQL command to create a table with the specified structure if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discharge_notes (
            id INTEGER PRIMARY KEY,  # Unique identifier for each record
            note TEXT NOT NULL,      # The discharge note text
            note_id TEXT,            # Identifier for the note
            subject_id TEXT,         # Identifier for the subject
            hadm_id TEXT,            # Admission identifier
            note_type TEXT,          # Type/category of the note
            note_seq TEXT,           # Sequence number for the note
            charttime TEXT,          # Time of charting the note
            storetime TEXT           # Time of storing the note
        )
    """)

    # Commit the transaction to save the changes
    conn.commit()
    # Close the connection to the database
    conn.close()


def split_records(text):
    """
    Split the raw text into individual records based on a specific delimiter ('Name: ').

    Args:
        text (str): The raw text containing multiple records.

    Returns:
        list: A list of individual records.
    """
    # Split the text into records based on the delimiter 'Name: ', and remove empty or invalid records
    records = [record.strip() for record in text.split('Name: ') if record and record != 'Name:']
    # Prepend "Name: " to each valid record before returning
    return ["Name: " + record for record in records if record]


def insert_discharge_note(note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, storetime):
    """
    Insert a single discharge note record into the database.

    Args:
        note (str): The discharge note text.
        note_id (str): Identifier for the note.
        subject_id (str): Identifier for the subject.
        hadm_id (str): Admission identifier.
        note_type (str): Type/category of the note.
        note_seq (str): Sequence number for the note.
        charttime (str): Time of charting the note.
        storetime (str): Time of storing the note.
    """
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(DATABASE_NAME)
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a SQL command to insert the discharge note record into the database
    cursor.execute("""
        INSERT INTO discharge_notes 
        (note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, storetime) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, storetime))

    # Commit the transaction to save the changes
    conn.commit()
    # Close the connection to the database
    conn.close()


# Initialize the database by calling the initialize_db function
initialize_db(DATABASE_NAME)

# Open the CSV file in read mode and create a DictReader object to read rows as dictionaries
with open(file_name, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Iterate through each row in the CSV file using tqdm to display a progress bar
    for row in tqdm(csv_reader):
        # Split the 'text' field in the current row into individual records
        individual_records = split_records(row['text'])
        # Iterate through each individual record and insert it into the database
        for record in individual_records:
            # Call the insert_discharge_note function to insert the record into the database
            insert_discharge_note(record, row['note_id'], row['subject_id'], row['hadm_id'], row['note_type'],
                                  row['note_seq'], row['charttime'], row['storetime'])
