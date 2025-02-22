import Levenshtein
import numpy as np
import json
from transformers import RobertaTokenizer, T5ForConditionalGeneration

# モデルの定義
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-small')

def complete_code(input_text, max_length=50):
    input_ids = tokenizer(input_text, return_tensors='pt').input_ids
    outputs = model.generate(input_ids, max_length=max_length, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def normalize_edit_distance(reference, hypothesis):
    edit_distance = Levenshtein.distance(reference, hypothesis)
    normalized_distance = edit_distance / max(len(reference), len(hypothesis))
    return normalized_distance

def evaluate_model(data):
    scores = []
    for input_text, reference in data:
        hypothesis = complete_code(input_text)
        distance = normalize_edit_distance(reference, hypothesis)
        scores.append(distance)
    average_score = np.mean(scores)
    return average_score

with open('../datasets/finetune_data/test.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Evaluate model
average_score = evaluate_model(data)
print("Average Normalized Edit Distance:", average_score)