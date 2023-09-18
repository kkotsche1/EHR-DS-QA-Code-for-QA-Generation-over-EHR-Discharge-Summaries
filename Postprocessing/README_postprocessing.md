# Project Documentation

This documentation provides a detailed overview of various Python scripts used to manipulate and analyze a dataset of medical records.

## Table of Contents
1. [json_postprocessing.py](#json_postprocessingpy)
2. [merge_db_to_json.py](#merge_db_to_jsonpy)
3. [counting_tokens.py](#counting_tokenspy)

## json_postprocessing.py

A Python script that contains various functions to process, clean, and manipulate JSON data, focusing especially on handling question and answer (QA) pairs within a dataset of medical records. Here, we detail the functionality of each function contained in the script:

### Functions
1. **replace_instances(text)**
   - Description: Replaces occurrences of specific prefixes like "Mr.", "Ms.", "Mrs.", and "Dr." with generic terms to anonymize data.
   - Parameters:
     - text (str): The input text containing instances to replace.
   - Returns:
     - (str): The text with the instances replaced.

2. **count_qa_pairs(json_file_path)**
   - Description: Count the total number of question and answer pairs in the JSON file.
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Prints the total number of notes and QA pairs in the console.

3. **extract_qa_pairs(text)**
   - Description: Extracts question and answer pairs from the given text.
   - Parameters:
     - text (str): The input text containing questions and answers in a specific format.
   - Returns:
     - list: A list of tuples where each tuple contains a question and its corresponding answer.

4. **reparse_qa_pairs(json_file_path)**
   - Description: Identifies and corrects improperly parsed question and answer pairs in the JSON file, which are found as a single answer.
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Modifies the JSON file in place to correct parsing errors.

5. **replace_mr_mrs(json_file_path)**
   - Description: Iterates through the JSON data and replaces any instance in both the question and answer strings with 'the patient' or 'the patient's'.
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Modifies the JSON file in place to replace specified instances.

6. **remove_special_token(json_file_path)**
   - Description: Iterates through the JSON data and removes any instance of the stop token `</s>` from the question and answer strings.
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Modifies the JSON file in place to remove special tokens.

7. **remove_underscore_patterns(json_file_path)**
   - Description: Removes question and answer pairs from the JSON data where either the question or the answer contains patterns "_" or "__" or "___".
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Modifies the JSON file in place to remove pairs with underscore patterns.

8. **remove_context_questions(json_file_path)**
   - Description: Removes question and answer pairs from the JSON data where the word "context" is found in the question.
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Modifies the JSON file in place to remove pairs with the word "context" in questions.

9. **remove_incomplete_answers(json_file_path)**
   - Description: Removes question and answer pairs from the JSON data where the answer does not end with a period (".").
   - Parameters:
     - json_file_path (str): The path to the JSON file.
   - Returns:
     - None: Modifies the JSON file in place to remove pairs with incomplete answers.

10. **remove_entry_without_qa(json_file_path)**
    - Description: Removes entries from the JSON data where the 'qa_pairs' list is empty.
    - Parameters:
         - json_file_path (str): The path to the JSON file.
    - Returns:
         - None: Modifies the JSON file in place to remove entries without question and answer pairs.

### How to Use
Set the `json_file_path` variable to the path of your JSON file. Uncomment the functions you want to use at the bottom of the script, and run the script to process the JSON file accordingly.

## merge_db_to_json.py 

This script merges data from multiple SQLite databases into a single JSON file. 

### Script Overview:
- **Importing Modules:**
  - sqlite3: A DB-API 2.0 implementation for SQLite databases.
  - json: A module for working with JSON data.
  - tqdm: A module providing a progress bar (currently not utilized).
  - ThreadPoolExecutor: A high-level interface for asynchronously executing callables (currently not utilized).

- **Function Definitions:**
  - get_data_from_db: Fetches notes and QA pairs from the database in batches, with an optional "8k" column for extended context.
  - check_8k_column: Checks if the "8k" column exists in the "discharge_notes" table of the database.
  - merge_data_to_json: Combines data from multiple databases and writes it to a JSON file.

- **Script Execution:**
  - Paths to the databases and the output JSON file are specified.
  - The merge_data_to_json function is called to merge data from the specified databases into a single JSON file.

- **Key Details:**
  - Operates in batches to process large data efficiently without consuming excessive memory.
  - Adapts to databases with varying structures, particularly regarding the presence of an "8k" column.
  - Utilizes a dictionary and a set to prevent duplication of notes and QA pairs.
  - Enhances performance of SQLite database operations using PRAGMA options.

## counting_tokens.py

This script is utilized to count the number of tokens in the notes and QA pairs contained within a JSON dataset. It uses the `transformers` library to tokenize the text data and compute the total and average number of tokens for notes and QA pairs separately.

### Usage
1. Ensure the `model_path` variable points to the correct path of your tokenizer model.
2. Specify the correct path to your JSON data file in the `with open` statement.
3. Run the script using a Python interpreter:
   ```sh
   python counting_tokens.py

### Output
The script will output the following metrics:

1. Total number of tokens in notes.
2. Total number of tokens in QA pairs.
3. Total number of notes and QA pairs processed.
4. Average number of tokens in notes and QA pairs.
