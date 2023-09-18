import sqlite3
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def get_data_from_db(db_path, offset, batch_size, has_8k_column):
    """
    Fetch data from the database.

    Parameters:
    db_path (str): The path to the database.
    offset (int): The offset to start fetching records from.
    batch_size (int): The number of records to fetch in each batch.
    has_8k_column (bool): Flag to indicate if the database has an "8k" column.

    Returns:
    tuple: A tuple containing notes and QA pairs fetched from the database.
    """
    with sqlite3.connect(db_path) as conn:
        # Setting PRAGMA options to enhance performance
        conn.execute("PRAGMA synchronous = OFF")
        conn.execute("PRAGMA journal_mode = MEMORY")
        cursor = conn.cursor()

        # Fetch notes with extended_context and new metadata fields
        if has_8k_column:
            cursor.execute(
                f"""SELECT id, note, COALESCE("8k", 0) AS extended_context, note_id, 
                    subject_id, hadm_id, note_type, note_seq, charttime, storetime 
                FROM discharge_notes LIMIT {batch_size} OFFSET {offset}""")
        else:
            cursor.execute(
                f"""SELECT id, note, 0 AS extended_context, note_id, 
                    subject_id, hadm_id, note_type, note_seq, charttime, storetime 
                FROM discharge_notes LIMIT {batch_size} OFFSET {offset}""")

        notes = cursor.fetchall()

        # Fetch QA pairs excluding truncated questions and answers
        cursor.execute(
            f"SELECT id, note_id, question, answer FROM qa_pairs WHERE question NOT LIKE '%Truncated%' AND answer NOT LIKE '%Truncated%' LIMIT {batch_size} OFFSET {offset}")
        qa_pairs = cursor.fetchall()

    return notes, qa_pairs


def check_8k_column(db_path):
    """
    Check if the "8k" column exists in the database.

    Parameters:
    db_path (str): The path to the database.

    Returns:
    bool: True if the "8k" column exists, False otherwise.
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(discharge_notes)")
        columns = cursor.fetchall()
        return any(column[1] == "8k" for column in columns)


def merge_data_to_json(db_paths, output_json_path, batch_size=1000):
    """
    Merge data from multiple databases and save it to a JSON file.

    Parameters:
    db_paths (list): A list of paths to the databases.
    output_json_path (str): The path to save the output JSON file.
    batch_size (int): The number of records to process in each batch (default is 1000).
    """
    note_dict = {}
    processed_qa_pairs = set()

    for db_path in db_paths:
        offset = 0
        has_8k_column = check_8k_column(db_path)

        while True:
            # Fetch data from the database in batches
            notes, qa_pairs = get_data_from_db(db_path, offset, batch_size, has_8k_column)
            if not notes and not qa_pairs:
                break

            for note in notes:
                if note[0] not in note_dict:
                    note_dict[note[0]] = {
                        'original_id': note[0],
                        'note': note[1],
                        'qa_pairs': [],
                        'extended_context': bool(note[2]),
                        'note_id': note[3],
                        'subject_id': note[4],
                        'hadm_id': note[5],
                        'note_type': note[6],
                        'note_seq': note[7],
                        'charttime': note[8],
                        'storetime': note[9]
                    }
                else:
                    # Update the extended_context value and new metadata fields
                    if note[2]:
                        note_dict[note[0]]['extended_context'] = True
                    # (You can also update other fields here if needed)

            # Process QA pairs and add them to the respective notes in note_dict
            for qa_pair in qa_pairs:
                serialized_qa_pair = json.dumps({'note_id': qa_pair[1], 'question': qa_pair[2], 'answer': qa_pair[3]})
                if serialized_qa_pair not in processed_qa_pairs:
                    if qa_pair[1] in note_dict:
                        note_dict[qa_pair[1]]['qa_pairs'].append({'question': qa_pair[2], 'answer': qa_pair[3]})
                        processed_qa_pairs.add(serialized_qa_pair)

            offset += batch_size

    # Filter notes which have QA pairs and save to JSON file
    filtered_notes = [v for k, v in note_dict.items() if v['qa_pairs']]
    with open(output_json_path, 'w') as json_file:
        json.dump(filtered_notes, json_file, indent=4)


# Paths to the databases and output JSON file
db_paths = ['../database_files/with_metadata/EHR_summary_notes.db', '../database_files/with_metadata/EHR_summary_notes_8k.db',
            '../database_files/with_metadata/EHR_summary_notes - Copy.db']
output_json_path = '../ehr_notes_qa_metadata_master_processed.json'

# Merging data from databases to JSON
merge_data_to_json(db_paths, output_json_path)
