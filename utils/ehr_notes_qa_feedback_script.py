import json
import random
import os

def get_feedback_on_note(note):
    print(f"Note ID: {note['original_id']}")
    print("Note:")
    print(note['note'])

    for qa_pair in note.get('qa_pairs', []):
        print("\nQuestion:")
        print(qa_pair['question'])
        print("Answer:")
        print(qa_pair['answer'])

        # Get feedback from user
        while True:
            feedback = input("Is this answer correct? (yes/no): ").strip().lower()
            if feedback in ['yes', 'no']:
                qa_pair['correct'] = feedback == 'yes'
                print("##########################################")
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    # Set the note as human verified as all QAs have been reviewed
    note['human_verified'] = True

    return note

# Load the data from the JSON file
file_path = '../ehr_notes_qa_metadata_master_processed.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Load verified notes from the verified JSON file if it exists
verified_file_path = "../ehr_notes_qa_verified.json"
if os.path.exists(verified_file_path):
    with open(verified_file_path, 'r') as file:
        verified_data = json.load(file)
else:
    verified_data = []

# Get a list of unverified notes
unverified_notes = [note for note in data if not note.get('human_verified') and note not in verified_data]

# Loop to get feedback on random notes until all are verified
while unverified_notes:
    # Select a random note
    note = random.choice(unverified_notes)

    # Get feedback on the note
    verified_note = get_feedback_on_note(note)

    # Remove the note from the list of unverified notes
    unverified_notes.remove(note)

    # Add the verified note to the verified data list and save it to the verified JSON file
    verified_data.append(verified_note)
    with open(verified_file_path, 'w') as file:
        json.dump(verified_data, file, indent=4)
    # Check if user wants to continue
    if unverified_notes:
        continue_feedback = input("Do you want to continue reviewing? (yes/no): ").strip().lower()

        if continue_feedback == 'no':
            break
    else:
        print("All notes have been reviewed.")
