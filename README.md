# EHR-DS-QA: A synthetic QA Dataset Derived from Medical Discharge Summaries for Enhanced Medical Information Retrieval Systems


This repository contains a dataset designed for training large language models specialized in retrieving information from health records through context-augmented generation. The data is extracted and structured from the MIMIC-IV-Note database and is available in two formats: JSON and CSV. Here, we describe the structure of both files along with a JSON example entry:

## Dataset Files

1. **discharge_notes_qa.json**
2. **discharge_notes_qa.csv**

## File Structure and Descriptions

### JSON Structure

The JSON file is structured as a list of dictionaries where each dictionary represents a medical discharge note. Here's the structure of each entry along with an example entry with placeholder data:

```json
{
    "original_id": "placeholder_original_id",
    "note": "placeholder_note_text",
    "qa_pairs": [
        {
            "question": "placeholder_question_text",
            "answer": "placeholder_answer_text",
            "correct": "placeholder_boolean"
        }
    ],
    "extended_context": "placeholder_boolean",
    "note_id": "placeholder_note_id",
    "subject_id": "placeholder_subject_id",
    "hadm_id": "placeholder_hadm_id",
    "note_type": "placeholder_note_type",
    "human_verified": "placeholder_boolean"
}
```

#### Fields:

-   **original_id**: (Integer) A unique identifier assigned during the creation of this dataset.
-   **note**: (String) The discharge summary text directly extracted from the MIMIC-IV-Note database.
-   **qa_pairs**: (List of Dictionaries) Each dictionary contains:
    -   **question**: (String) A question related to the patient's case.
    -   **answer**: (String) An answer to the corresponding question.
    -   **correct**: (Boolean, optional) Indicates the verified accuracy of the Q&A pair.
-   **extended_context**: (Boolean) Indicates whether the note contains more than 3000 tokens.
-   **note_id**: (String) A unique identifier for each note.
-   **subject_id**: (String) A de-identified patient identifier.
-   **hadm_id**: (String) A unique identifier for each hospital admission.
-   **note_type**: (String) Indicates the category of the note, "DS" signifies a Discharge Summary.
-   **human_verified**: (Boolean, optional) Denotes if all QA pairs associated with the note have been verified by humans.


### CSV Structure

The CSV file is generated from the JSON data, where each key from the JSON dictionary becomes a column in the CSV file. Nested structures such as `qa_pairs` (a list of dictionaries in the JSON) will be converted to a string representation and stored in a single cell in the CSV file. This is generated using a Python script, which reads the keys from the JSON data to form the headers of the CSV, and then writes each entry as a row in the CSV file. The fields are the same as described in the JSON structure section.

Here's an example of how the data would be structured in the CSV:

```csv
original_id,note,qa_pairs,extended_context,note_id,subject_id,hadm_id,note_type,human_verified
placeholder_original_id,"placeholder_note_text","[{""question"": ""placeholder_question_text"", ""answer"": ""placeholder_answer_text"", ""correct"": ""placeholder_boolean""}]",placeholder_boolean,placeholder_note_id,placeholder_subject_id,placeholder_hadm_id,placeholder_note_type,placeholder_boolean
```

## Source

The original data has been extracted from the MIMIC-IV-Note dataset. 

> Johnson, A., Pollard, T., Horng, S., Celi, L. A., & Mark, R. (2023). MIMIC-IV-Note: Deidentified free-text clinical notes (version 2.2). PhysioNet. [https://doi.org/10.13026/1n74-ne17](https://doi.org/10.13026/1n74-ne17)

> Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.

## Contribution and Contact

For contributions or updates to the dataset, please contact Konstantin Kotschenreuther at [kkotsche1@gmail.com](mailto:kkotsche1@gmail.com). The GitHub repository for this project can be found [here](https://github.com/kkotsche1/EHR-DS-QA-Code-for-QA-Generation-over-EHR-Discharge-Summaries).

### Version: 1.0.0