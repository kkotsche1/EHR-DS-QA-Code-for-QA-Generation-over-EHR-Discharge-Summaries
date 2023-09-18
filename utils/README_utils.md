# EHR Notes QA Feedback Script

## Description
This script facilitates the review and verification process of EHR (Electronic Health Records) notes. It allows users to provide feedback on question-answer pairs in the notes, and stores the verification status of each note in a JSON file. The script selects unverified notes at random, allows users to mark whether the answers are correct, and keeps track of which notes have been human verified.

## Installation

No installation is needed as the script is a standalone Python script. Just make sure to have Python 3.x installed in your system.

## Usage

To use the script, simply run it from your terminal or an IDE. It will prompt you with the contents of a note and ask you to verify if the answer to each question in the note is correct. 

Here are the steps on how to use it:

1. Ensure that the JSON files (`ehr_notes_qa_metadata_master_processed.json` and `ehr_notes_qa_verified.json`) are in the correct relative paths as indicated in the script.
2. Run the script: `python ehr_notes_qa_feedback_script.py`
3. The script will display a note and ask you to verify the answer to each question in the note.
4. Enter 'yes' or 'no' to indicate whether the answer is correct or not.
5. After reviewing all the questions in a note, you will have the option to continue reviewing more notes or exit.

## Features

- Random selection of unverified notes for review
- Input validation for the feedback (accepts only 'yes' or 'no')
- The ability to continue or stop the review process at the end of reviewing a note
- Saves verified notes to a separate JSON file to keep track of the progress

## File Structure

- `ehr_notes_qa_feedback_script.py`: The main script file.
- `../ehr_notes_qa_metadata_master_processed.json`: The master data file containing all notes.
- `../ehr_notes_qa_verified.json`: The file where verified notes are stored.

## Functions

### `get_feedback_on_note(note)`
This function accepts a note (dictionary) as an argument and returns the note with updated verification status. It displays the note ID, the note itself, and iterates through the list of question-answer pairs, prompting the user to provide feedback on the correctness of each answer.

