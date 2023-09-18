from transformers import AutoTokenizer
import json
from tqdm import tqdm

model_path = "../OpenAssistant-Llama2-13B-Orca-8K-3319-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True, device="cuda")


# Load the JSON data
with open('../ehr_notes_qa_master.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize counters for the total number of tokens
total_note_tokens = 0
total_qa_tokens = 0
note_counter = 0
qa_counter = 0

# Iterate over each entry in the data
for entry in tqdm(data):
    # Tokenize the note text and add the number of tokens to the total note tokens count
    encoding = tokenizer(entry['note'], return_tensors="pt")
    total_note_tokens += len(encoding["input_ids"][0])
    note_counter += 1

    # Iterate over each QA pair in the entry
    for qa_pair in entry['qa_pairs']:
        qa_counter += 1
        # Tokenize the question and answer texts and add the number of tokens to the total QA pairs tokens count
        question_encoding = tokenizer(qa_pair['question'], return_tensors="pt")
        answer_encoding = tokenizer(qa_pair['answer'], return_tensors="pt")
        total_qa_tokens += len(question_encoding["input_ids"][0]) + len(answer_encoding["input_ids"][0])

# Print the total number of tokens in the notes and in the QA pairs
print(f"Total number of tokens in notes: {total_note_tokens}")
print(f"Total number of tokens in QA pairs: {total_qa_tokens}")
print("############################################")

# Print the total number of tokens in the notes and in the QA pairs
print(f"Total number of notes: {note_counter}")
print(f"Total number of QA pairs: {qa_counter}")

print("############################################")

# Print the average number of tokens in the notes and in the QA pairs
print(f"Average number of tokens in notes: {total_note_tokens/note_counter}")
print(f"Average number of tokens in QA pairs: {total_qa_tokens/qa_counter}")