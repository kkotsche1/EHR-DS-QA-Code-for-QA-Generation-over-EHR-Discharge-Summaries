import json
import re


#USED BY THE REPLACE MR AND MRS FUNCTION
def replace_instances(text):
    """Replace instances with 'the patient', 'the patient's', 'the doctor', or 'the doctor's' as appropriate.

    Args:
    text (str): The input text containing the instances to replace.

    Returns:
    str: The text with the instances replaced.
    """
    text = re.sub(r"Mr\.\s*_+'s", "the patient's", text)
    text = re.sub(r"Ms\.\s*_+'s", "the patient's", text)
    text = re.sub(r"Mrs\.\s*_+'s", "the patient's", text)
    text = re.sub(r"Dr\.\s*_+'s", "the doctor's", text)

    text = re.sub(r"Mr\.\s*_+", "the patient", text)
    text = re.sub(r"Ms\.\s*_+", "the patient", text)
    text = re.sub(r"Mrs\.\s*_+", "the patient", text)
    text = re.sub(r"Dr\.\s*_+", "the doctor", text)

    return text

def count_qa_pairs(json_file_path):
    """Count the total number of question and answer pairs in the JSON file.

    Args:
    json_file_path (str): The path to the JSON file.

    Returns:
    int: The total number of question and answer pairs.
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        print("Number of Notes", len(data))
        print("Number of QA Pairs", sum(len(item['qa_pairs']) for item in data))


#USED BY THE REPARSE_QA_PAIRS FUNCTION
def extract_qa_pairs(text):
    """
    This function extracts question and answer pairs from the given text.

    Args:
        text (str): The input text containing questions and answers in a specific format.

    Returns:
        list: A list of tuples where each tuple contains a question and its corresponding answer.
    """

    # Check if the text contains the strings 'Question:' and 'Answer:' to determine the format for extraction.
    if "Question:" in text and "Answer:" in text:
        # Use regular expressions to find all matches where 'Question:' and 'Answer:' are present with variable whitespace between them and the actual question and answer text.
        qa_pairs_raw = re.findall(r'Question:\s*(.*?)\s*Answer:\s*(.*?)(?=(?:\s*Question:)|(?=\d+\.)|$)', text,
                                  re.DOTALL)

        # If no matches are found in the above format, check for another format where 'Question:' and 'Answer:' are on separate lines followed by the actual question and answer text.
        if not qa_pairs_raw:
            qa_pairs_raw = re.findall(r'Question:\s*(.*?)\nAnswer:\s*(.*?)(?=\nQuestion:|$)', text, re.DOTALL)
    else:
        # If the 'Question:' and 'Answer:' labels are not found, try to find matches in a numbered format where questions and answers are separated by newline characters.
        qa_pairs_raw = re.findall(r'\d+\.\s(.*?)\n\s*(.*?)(?=(?:\n\s*\d+\.)|$)', text, re.DOTALL)

    # Clean up the extracted question and answer pairs by removing leading and trailing whitespaces and removing the 'Question:' and 'Answer:' labels from the actual text.
    results = [(q.strip().replace("Question: ", ""), a.strip().replace("Answer: ", "")) for q, a in qa_pairs_raw]

    # If more than one pair is extracted, return all pairs except the last one. If only one or no pairs are extracted, return all extracted pairs.
    if len(results) > 1:
        return results[:-1]
    else:
        return results

#A FUNCTION THAT LOOKS THROUGH THE ANSWERS IN THE JSON TO CHECK IF ANY QUESTION AND ANSWER PAIRS WERE IMPROPERLY PARSED LEADING TO THEM BEING DEPOSITED AS ONE SINGLE ANSWER
#USES THE EXTRACT QA PAIRS FUNCTION
def reparse_qa_pairs(json_file_path):
    """Find and print the first fifty instances of question and answer pairs containing "Mr." or "Mrs." in the JSON file.

    Args:
    json_file_path (str): The path to the JSON file.

    Returns:
    None
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        counter = 0

        for i, item in enumerate(data):
            qa_pairs = item.get('qa_pairs', [])
            for j, qa_pair in enumerate(qa_pairs):
                question = qa_pair.get('question', '')
                answer = qa_pair.get('answer', '')
                if ("question" in answer or "answer" in answer or 'Question:' in answer or "Answer:" in answer) and "1." in answer:
                    extracted_qa_pairs = extract_qa_pairs(answer)
                    if len(extracted_qa_pairs) < 2:
                        continue
                    else:
                        if len(qa_pairs) == 1:
                            #Replacing if incorrectly parsed QA pairs is only entry
                            item['qa_pairs'] = extracted_qa_pairs
                        else:
                            #Extending if wrongly parsed answer identified among numerous qa pairs
                            item['qa_pairs'].pop(j).extend(extracted_qa_pairs)

    # Save the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

#REPLACING INSTANCES OF MR MRS DR etc WITH PATIENT, THE DOCTOR etc.
def replace_mr_mrs(json_file_path):
    """Iterate through the JSON and replace any instance in both the question and answer strings with 'the patient' or 'the patient's'.

    Args:
    json_file_path (str): The path to the JSON file.

    Returns:
    None
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for i, item in enumerate(data):
        qa_pairs = item.get('qa_pairs', [])
        for j, qa_pair in enumerate(qa_pairs):
            question = qa_pair.get('question', '')
            answer = qa_pair.get('answer', '')

            # Replacing instances in the question and answer strings
            qa_pair['question'] = replace_instances(question)
            qa_pair['answer'] = replace_instances(answer)

    # Saving the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

#REMOVES </s> FROM OUR STRINGS WHICH IS A STOP TOKEN THAT WAS SOMETIMES INCLUDED IN OUR OUTPUT
def remove_special_token(json_file_path):
    """Iterate through the JSON and replace any instance of the stop token.

    Args:
    json_file_path (str): The path to the JSON file.

    Returns:
    None
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for i, item in enumerate(data):
        qa_pairs = item.get('qa_pairs', [])
        for j, qa_pair in enumerate(qa_pairs):
            question = qa_pair.get('question', '')
            answer = qa_pair.get('answer', '')

            # Remove the token "</s>" from question and answer strings
            qa_pair['question'] = question.replace("</s>", "")
            qa_pair['answer'] = answer.replace("</s>", "")

    # Saving the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

#REMOVES QA PAIRS WHERE EITHER THE QUESTION OR THE ANSWER CONTAINS AN INSTANCE OF DEIDENTIFIED INFORMATION DENOTED BY "_+"
def remove_underscore_patterns(json_file_path):
    """Iterate through the JSON and remove any question and answer pair where either the question or the answer contains patterns "_" or "__" or "___".

    Args:
    json_file_path (str): The path to the JSON file.

    Returns:
    None
    """
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    for i, item in enumerate(data):
        qa_pairs = item.get('qa_pairs', [])

        new_qa_pairs = []
        for qa_pair in qa_pairs:
            if isinstance(qa_pair, dict):
                question = qa_pair.get('question', '')
                answer = qa_pair.get('answer', '')

                # Check if patterns are present in the question or answer
                if not (re.search(r'_{1,3}', question) or re.search(r'_{1,3}', answer)):
                    new_qa_pairs.append(qa_pair)

        # Update qa_pairs with the pairs that didn't contain the patterns
        item['qa_pairs'] = new_qa_pairs

    # Saving the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def remove_context_questions(json_file_path):
    """
    Iterate through the JSON file and remove any question and answer pair where
    the word "context" is found in the question.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        None
    """
    # Opening the JSON file and loading the data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Iterating through each item in the data
    for i, item in enumerate(data):
        # Extracting the qa_pairs section from each item
        qa_pairs = item.get('qa_pairs', [])

        new_qa_pairs = []
        # Iterating through each pair in the qa_pairs section
        for qa_pair in qa_pairs:
            if isinstance(qa_pair, dict):
                # Extracting the question from the pair
                question = qa_pair.get('question', '')

                # Checking if the word "context" is not present in the question
                if "context" not in question.lower():
                    # If "context" is not found, adding the pair to the new list
                    new_qa_pairs.append(qa_pair)

        # Updating the qa_pairs section with the new list which doesn't contain the word "context" in questions
        item['qa_pairs'] = new_qa_pairs

    # Saving the updated data back to the JSON file with proper formatting
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def remove_incomplete_answers(json_file_path):
    """
    Iterate through the JSON file and remove any question and answer pair where
    the answer does not end with a period (".").

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        None
    """
    # Opening the JSON file and loading the data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Iterating through each item in the data
    for i, item in enumerate(data):
        # Extracting the qa_pairs section from each item
        qa_pairs = item.get('qa_pairs', [])

        new_qa_pairs = []
        # Iterating through each pair in the qa_pairs section
        for qa_pair in qa_pairs:
            if isinstance(qa_pair, dict):
                # Extracting the answer from the pair
                answer = qa_pair.get('answer', '')

                # Checking if the answer ends with a period
                if answer.endswith('.'):
                    # If it ends with a period, adding the pair to the new list
                    new_qa_pairs.append(qa_pair)

        # Updating the qa_pairs section with the new list which contains only answers ending with a period
        item['qa_pairs'] = new_qa_pairs

    # Saving the updated data back to the JSON file with proper formatting
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def remove_entry_without_qa(json_file_path):
    """
    Iterate through the JSON file and remove any entries where the 'qa_pairs'
    list is empty.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        None
    """
    try:
        # Step 1: Open the JSON file and load the data
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Step 2: Filter the data to retain only entries with non-empty 'qa_pairs' list
        new_data = [item for item in data if item.get('qa_pairs')]

        # Step 3: Save the updated data back to the JSON file with proper formatting
        with open(json_file_path, 'w') as json_file:
            json.dump(new_data, json_file, indent=4)

    except Exception as e:
        # If an error occurs, print the error message
        print(f"An error occurred: {e}")

json_path = "../ehr_notes_qa_metadata_master_processed.json"

count_qa_pairs(json_path)
# replace_mr_mrs(json_path)
# remove_special_token(json_path)
# reparse_qa_pairs(json_path)
# remove_underscore_patterns(json_path)
#remove_context_questions(json_path)
#remove_incomplete_answers(json_path)
remove_entry_without_qa(json_path)
count_qa_pairs(json_path)
