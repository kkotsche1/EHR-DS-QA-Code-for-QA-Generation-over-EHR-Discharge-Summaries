import sqlite3
import requests
import traceback
import os
from transformers import AutoTokenizer
import re

os.chdir("/exllama")

from model import ExLlama, ExLlamaCache, ExLlamaConfig
from tokenizer import ExLlamaTokenizer
from generator import ExLlamaGenerator
import torch

os.chdir("../")

### MODEL INITIALIZATION

tokenizer_model_path = "/path/to/OpenOrca-Platypus2-13B-GPTQ/tokenizer.model"
model_config_path = "/path/to/OpenOrca-Platypus2-13B-GPTQ/config.json"
model_path = "/path/to/OpenOrca-Platypus2-13B-GPTQ/model.safetensors"

config = ExLlamaConfig(model_config_path)
config.model_path = model_path
config.max_seq_len = 4096

model = ExLlama(config)
cache = ExLlamaCache(model)

tokenizer = ExLlamaTokenizer(tokenizer_model_path)
generator = ExLlamaGenerator(model, tokenizer, cache)
generator.settings.temperature = 0.5

### FUNCTION TO GET RESPONSE FROM LARGE LANGUAGE MODEL

def get_llm_response(prompt_template):
    torch.set_grad_enabled(False)
    torch.cuda._lazy_init()

    # Sending the prompt to the model for inference and capturing the response in the response string variable
    gen_tokens = 768
    text = generator.generate_simple(prompt_template, max_new_tokens=gen_tokens)
    llm_response = text.split("### Response:")[-1].strip()
    return llm_response

### FUNCTION TO PLACE NOTE WITHIN PROMPT TEMPLATE FOR LLM PROCESSING

def format_prompt(clinical_note):
    prompt = f"""
    ### Instruction:

    - Generate question and answer pairs from the provided context.
    - Provide an answer to each question with all relevant and necessary information. 
    - Do not include any additional information that is not included in the given context.
    - Do not reference the context in your questions.
    - Provide your response formatted as follows: "Question: This is a sample question\nAnswer: This is a sample answer".

    Context:

    {clinical_note}

    ### Response:"""

    return prompt

### FUNCTION TO TRUNCATE PROMPT TO 3000 TOKENS IF NECESSARY
tokenizer = AutoTokenizer.from_pretrained("TheBloke/OpenOrca-Platypus2-13B-GPTQ", use_fast=True)
def truncate_prompt(prompt, truncation_length=3000):
    encoding = tokenizer.encode(prompt, truncation=True, max_length=truncation_length)
    decode = tokenizer.decode(encoding)
    was_truncated = len(encoding) == truncation_length

    if not decode.endswith("### Response:"):
        prompt = decode + """

### Response:"""
        prompt = prompt.replace("<s>", "")

    return prompt, was_truncated

### FUNCTION TO EXTRACT QA PAIRS FROM CONTINUOUS STRING RETURNED BY LLM CALL

def extract_qa_pairs(text):
    # Check for the presence of 'Question:' and 'Answer:' in the text to determine the format.
    if "Question:" in text and "Answer:" in text:
        # Find all matches for the format where 'Question:' and 'Answer:' are present with variable whitespace.
        qa_pairs_raw = re.findall(r'Question:\s*(.*?)\s*Answer:\s*(.*?)(?=(?:\s*Question:)|(?=\d+\.)|$)', text,
                                  re.DOTALL)

        # If no matches are found, check for the other format where 'Question:' and 'Answer:' are in separate lines.
        if not qa_pairs_raw:
            qa_pairs_raw = re.findall(r'Question:\s*(.*?)\nAnswer:\s*(.*?)(?=\nQuestion:|$)', text, re.DOTALL)
    else:
        # Match the numbered format without the explicit 'Question:' label.
        qa_pairs_raw = re.findall(r'\d+\.\s(.*?)\n\s*(.*?)(?=(?:\n\s*\d+\.)|$)', text, re.DOTALL)

    # Strip leading and trailing whitespaces and store the question and answer pairs in a list.
    results = [(q.strip(), a.strip()) for q, a in qa_pairs_raw]

    if len(results) > 1:
        return results[:-1]
    else:
        return results

### QA GENERATION PIPELINE FUNCTION

def generate_qa(clinical_note):

        try:
            clinical_note = "Allergies:" + clinical_note.split("Allergies:")[-1]
        except:
            clinical_note = clinical_note

        # formatting prompt
        prompt = format_prompt(clinical_note)

        # truncating prompt if necessary
        prompt, was_truncated = truncate_prompt(prompt)

        if was_truncated:
            return [], True

        # getting LLM response
        response = get_llm_response(prompt)

        # Parsing the response string for QA pairs
        qa_pairs = extract_qa_pairs(response)

        return qa_pairs, was_truncated

def get_connection(database_name="../EHR_summary_notes.db"):
    """Return a connection to the database."""
    return sqlite3.connect(database_name)

from tqdm import tqdm



def process_notes_and_add_qa_pairs():
    """Iterate through all notes in the radiology_notes table and add qa_pairs for each note."""

    # Select all notes from discharge_notes table
    select_cursor.execute("SELECT id, note FROM discharge_notes")

    for note_id, note_content in select_cursor:  # Using the select_cursor as an iterator
            try:
                # Check if the note_id already has entries in the qa_pairs table
                check_cursor.execute("SELECT COUNT(*) FROM qa_pairs WHERE note_id=?", (note_id,))
                entry_count = check_cursor.fetchone()[0]

                if entry_count > 0:
                    # If there are already Q&A pairs for this note_id, skip processing
                    continue

                # API Call to backend to generate qa pairs
                qa_pairs, was_truncated = generate_qa(note_content)
                if was_truncated:
                    truncated = 1
                else:
                    truncated = 0

                if len(qa_pairs) > 0:
                    for question, answer in qa_pairs:

                            # Inserting into the qa_pairs table
                            insert_cursor.execute("""
                                INSERT INTO qa_pairs (note_id, question, answer, truncated)
                                VALUES (?, ?, ?, ?)
                            """, (note_id, question.replace("Question: ", ""), answer.replace("Answer: ", ""), truncated))

                conn.commit()  # Committing the new inserts
            except:
                continue

conn = get_connection()
select_cursor = conn.cursor()
insert_cursor = conn.cursor()
check_cursor = conn.cursor()
process_notes_and_add_qa_pairs()
conn.close()