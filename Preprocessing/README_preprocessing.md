# Preprocessing Folder

This folder contains scripts that are essential for the initial preprocessing phase of the project. The preprocessing is a crucial step as it involves converting raw data from CSV files into a structured database format which can be used for further analysis and operations.

## File Description

### `create_database_from_csv.py`

This Python script is responsible for creating a database from the data present in a CSV file and populating it with discharge notes metadata. The script performs the following operations:

1. **Database Initialization**:
   Initializes the database with the necessary table structure to store discharge notes metadata. The table contains columns such as note, note_id, subject_id, hadm_id, note_type, note_seq, charttime, and storetime.

2. **Reading Data from CSV**:
   Reads data from a predefined CSV file (`discharge.csv`) which contains discharge notes information.

3. **Data Insertion**:
   Inserts individual discharge notes records into the database after splitting the text field into individual records based on a specific delimiter.

4. **Error Handling and Progress Display**:
   Utilizes the `tqdm` module to display the progress of the data insertion process, helping users to visualize the process completion time.

### How to Run

To execute the script, navigate to the "Preprocessing" folder in a terminal and run the command:

```sh
python create_database_from_csv.py