# stats.py

This script is used to compute and display various statistics from a dataset of medical records stored in a JSON file. The statistics computed include details like the number of question and answer pairs, the number of discharge summaries, word counts, and more.

## Dependencies

The script requires the following Python packages:
- `json` (standard library)
- `nltk`
- `numpy`

You can install the necessary packages with the following command:
```sh
pip install nltk numpy
```

## Usage
To use the script, ensure that it is in the same directory as the JSON data file ('../ehr_notes_qa_metadata_master_processed.json') and run the script with a Python interpreter:
```sh
python stats.py
```

## Details
The script computes and prints the following statistics:

- Total QA Pairs: The total number of question and answer pairs present in the data.
- Total Discharge Summaries: The total number of discharge summaries found in the data.
- Unique Patients: The number of unique patients in the data.
- Unique Hospital Admissions: The number of unique hospital admissions documented in the data.
- Percentage of Notes Exceeding 3000 Tokens: The percentage of notes where the word count exceeds 3000 tokens.
- Average Word Count: The average word count of notes in the data.
- Median Word Count: The median word count of notes in the data.
- Range of Word Count: The range of word counts found in the data, i.e., the minimum and maximum word counts.