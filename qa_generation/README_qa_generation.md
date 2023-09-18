# QA Generation Script

This script, `qa_generation.py`, is designed to generate question and answer pairs from clinical notes. It uses a pre-trained language model to understand and extract relevant information from the given clinical notes and constructs Q&A pairs accordingly.

## Features

1. Utilizes a pre-trained language model for generating question and answer pairs.
2. Automatically truncates prompts to a certain length to accommodate the model's maximum sequence length.
3. Adds generated Q&A pairs to a SQLite database, with handling for already-processed notes.

## Setup

To set up the script for running, follow these steps:

### Step 1: Requirements
Ensure you have the necessary Python packages installed:
```bash
pip install requests transformers torch sqlite3
```

### Step 2: Model Files
Place the required model files (tokenizer, configuration, and model weights) at the specified paths:

- Tokenizer: /path/to/OpenOrca-Platypus2-13B-GPTQ/tokenizer.model
- Model Config: /path/to/OpenOrca-Platypus2-13B-GPTQ/config.json
- Model Weights: /path/to/OpenOrca-Platypus2-13B-GPTQ/model.safetensors

### Step 3: Database 
Ensure the SQLite database (EHR_summary_notes.db) is correctly set up and located at the specified path (../EHR_summary_notes.db).

## Functions
The script contains several functions, which are briefly described below:

- get_llm_response(prompt_template): Gets a response from the large language model.
- format_prompt(clinical_note): Formats the clinical note into a prompt template for the language model.
- truncate_prompt(prompt, truncation_length=3000): Truncates the prompt to a specific length if necessary.
- extract_qa_pairs(text): Extracts Q&A pairs from the response string.
- generate_qa(clinical_note): The main function for generating Q&A pairs from a clinical note.
- get_connection(database_name="../EHR_summary_notes.db"): Gets a connection to the SQLite database.
- process_notes_and_add_qa_pairs(): Processes all notes in the database and adds generated Q&A pairs.

# QA Generation 8K Script

This script, `qa_generation_8k.py`, is designed to generate question and answer pairs from extended clinical notes. It leverages a pre-trained large language model with 8K context handling capacity, making it capable of processing larger clinical notes more efficiently. The script also contains functions for database connectivity and handling truncated notes from a previous process.

## Features

1. Utilizes a pre-trained large language model with 8K context capacity for generating question and answer pairs.
2. Automatically manages CUDA memory to handle large data processing efficiently.
3. Includes functionality to process previously truncated notes in the database.
4. Adds generated Q&A pairs to a SQLite database.

## Setup

To setup the script for running, follow these steps:

### Step 1: Requirements
Ensure you have the necessary Python packages installed:
```bash
pip install requests transformers torch sqlite3
```

### Step 2: Model Files
Specify the path to the pre-trained model files in the model_path variable:
- model_path = "/path/to/OpenAssistant-Llama2-13B-Orca-8K-3319-GPTQ"

### Step 3: Database 
Ensure the SQLite database (EHR_summary_notes_8k.db) is correctly set up and located at a location accessible by the script.

## Functions
The script contains several functions, which are briefly described below:

- ntk_scaled_init: A modification to the Llama Rotary Embedding initialization to scale according to the 8K context model requirements.
- get_llm_response: Utilizes the large language model to generate responses to the given prompts.
- format_new_prompt: Formats the clinical note into a specific template for processing by the large language model.
- extract_qa_pairs: Extracts Q&A pairs from the string returned by the large language model.
- generate_qa: The main function for generating Q&A pairs from a clinical note.
- get_connection: Establishes a connection to the SQLite database.
- get_truncated_notes: Processes all notes in the database and adds generated Q&A pairs, with special handling for notes that were previously truncated due to length limitations.