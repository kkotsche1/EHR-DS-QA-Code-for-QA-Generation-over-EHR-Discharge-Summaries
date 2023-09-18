import json
from nltk.tokenize import word_tokenize
import nltk
import numpy as np

nltk.download('punkt')

with open('../ehr_notes_qa_metadata_master_processed.json', 'r') as f:
    data = json.load(f)


total_qa_pairs = sum(len(item['qa_pairs']) for item in data)
total_summaries = len(data)
normal_length_context_notes = len([item for item in data if item["extended_context"] == False])
extended_length_context_notes = len([item for item in data if item["extended_context"] == True])
non_extended_qas = sum(len(item['qa_pairs']) for item in data if item["extended_context"] == False)
extended_qas = sum(len(item['qa_pairs']) for item in data if item["extended_context"] == True)


unique_patients = len(set(item['subject_id'] for item in data))
unique_admissions = len(set(item['hadm_id'] for item in data))
notes_exceeding_3000_tokens = sum(1 for item in data if item['extended_context'])
percentage_exceeding_3000_tokens = (notes_exceeding_3000_tokens / total_summaries) * 100
word_counts = [len(word_tokenize(item['note'])) for item in data]
average_word_count = np.mean(word_counts)
median_word_count = np.median(word_counts)
range_word_count = (min(word_counts), max(word_counts))

print(f"Total QA Pairs: {total_qa_pairs}")
print(f"Total Discharge Summaries: {total_summaries}")
print(f"Average Word Count: {average_word_count:.2f}")
print(f"Median Word Count: {median_word_count}")
print(f"Range of Word Count: {range_word_count}")
print(f"Unique Patients: {unique_patients}")
print(f"Unique Hospital Admissions: {unique_admissions}")
print(f"Percentage of Notes Exceeding 3000 Tokens: {percentage_exceeding_3000_tokens:.2f}%")
print(f"Normal length notes {normal_length_context_notes}")
print(f"Extended length notes {extended_length_context_notes}")
print(f"Standard context number of QA pairs: {non_extended_qas}")
print(f"Extended context number of QA pairs: {extended_qas}")