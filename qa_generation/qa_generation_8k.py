import sqlite3
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
import transformers
import re


### INITIALIZATION OF NTK_SCALED ROPE EMBEDDING FUNCTIONALITY
old_init = transformers.models.llama.modeling_llama.LlamaRotaryEmbedding.__init__
def ntk_scaled_init(self, dim, max_position_embeddings=2048, base=10000, device=None):

    #The method is just these three lines
    max_position_embeddings = 8096
    a = 4 #Alpha value
    base = base * a ** (dim / (dim-2)) #Base change formula

    old_init(self, dim, max_position_embeddings, base, device)

transformers.models.llama.modeling_llama.LlamaRotaryEmbedding.__init__ = ntk_scaled_init

###INITIALIZING MODEL WITH 8K CONTEXT
model_path = "/path/to/OpenAssistant-Llama2-13B-Orca-8K-3319-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")

generation_config = GenerationConfig(
)

### FUNCTION TO GET RESPONSE FROM LARGE LANGUAGE MODEL
def get_llm_response(prompt):
    encoding = tokenizer(prompt, return_tensors="pt")
    input_ids = encoding["input_ids"].to("cuda")

    if len(encoding["input_ids"][0]) > 6000:
        return ""

    torch.set_grad_enabled(False)
    torch.cuda._lazy_init()

    with torch.no_grad():
        result = model.generate(
            input_ids=input_ids,
            generation_config=generation_config,
            return_dict_in_generate=False,
            output_scores=False,
            max_new_tokens=768,
        )

    # Move result tensor back to CPU
    result = result.cpu()

    # Clear CUDA cache
    torch.cuda.empty_cache()

    decoded_output = tokenizer.decode(result[0][len(input_ids[0]):])

    return decoded_output

### FUNCTION TO FORMAT THE NOTE FOR THE 8K CONTEXT MODEL

def format_new_prompt(clinical_note):
    system_message = "You are an AI assistant that follows instruction extremely well. Help as much as you can."
    user_prompt = f"""\n- Generate professional physician level question and answer pairs from the context below.
- Generate AT LEAST 5 question and answer pairs.
- Provide an answer to each question with all relevant and necessary information. 
- Do not include any additional information that is not included in the given context.
- Do not reference the context in your questions.
- Provide your response formatted as follows: "Question: This is a sample question\nAnswer: This is a sample answer".
Context:

{clinical_note}
"""
    prompt = f"""<|system|>{system_message}</s><|prompter|>{user_prompt}</s><|assistant|>"""

    return prompt


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
        prompt = format_new_prompt(clinical_note)
        # getting LLM response
        response = get_llm_response(prompt)

        # Parsing the response string for QA pairs
        qa_pairs = extract_qa_pairs(response)

        return qa_pairs

def get_connection(database_name="EHR_summary_notes_8k.db"):
    """Return a connection to the database."""
    return sqlite3.connect(database_name)


def get_truncated_notes():

    """Iterate through all notes in the discharge_notes table and add qa_pairs for each note that was previously skipped due to being longer than 3k tokens."""
    conn = get_connection()
    select_cursor = conn.cursor()
    insert_cursor = conn.cursor()

    # Select all truncated noted_ids from qa_pairs table
    select_cursor.execute("SELECT note_id FROM qa_pairs WHERE question = 'Truncated'")

    noted_ids = select_cursor.fetchall()

    for noted_id in noted_ids:
        try:
            noted_id = noted_id[0]  # Extract the integer from the tuple

            select_cursor.execute('SELECT "8k" FROM discharge_notes WHERE id = ?', (noted_id,))
            result = select_cursor.fetchone()

            if result:
                value_8k = result[0]

                if value_8k == 1:
                    continue

            check_cursor = conn.cursor()
            print(noted_id)
            # Find the matching note from the discharge_notes table
            check_cursor.execute("SELECT note FROM discharge_notes WHERE id = ?", (noted_id,))

            result = check_cursor.fetchone()
            if result:
                note = result[0]  # Extract the note from the result tuple

                # API Call to backend to generate qa pairs
                qa_pairs = generate_qa(note)

                truncated=2 #Placeholder

                if len(qa_pairs) > 0:

                    # Update the 8k column value to 1 for the current noted_id
                    update_cursor = conn.cursor()
                    update_cursor.execute('UPDATE discharge_notes SET "8k" = 1 WHERE id = ?', (noted_id,))
                    for question, answer in qa_pairs:
                        # Inserting into the qa_pairs table
                        insert_cursor.execute("""
                                INSERT INTO qa_pairs (note_id, question, answer, truncated)
                                VALUES (?, ?, ?, ?)
                            """, (noted_id, question.replace("Question: ", ""), answer.replace("Answer: ", ""), truncated))

                conn.commit()  # Committing the new inserts

        except:
            print("EXCEPTION", noted_id)
    conn.close()

if __name__ == "__main__":

    get_truncated_notes()

