import json
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import RobertaTokenizer, T5ForConditionalGeneration

# モデルの定義
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-small')

def complete_code(input_text, max_length=50):
    input_ids = tokenizer(input_text, return_tensors='pt').input_ids
    outputs = model.generate(input_ids, max_length=max_length, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def calculate_bleu(reference, hypothesis, n):
    reference_tokens = reference.split()
    hypothesis_tokens = hypothesis.split()
    weights = tuple([1.0/n] * n + [0.0] * (4-n))
    bleu_score = sentence_bleu([reference_tokens], hypothesis_tokens, weights=weights, smoothing_function=SmoothingFunction().method1)
    return bleu_score

def evaluate_model(data):
    scores_1gram = []
    scores_2gram = []
    scores_3gram = []
    scores_4gram = []

    for input_text, reference in data:
        hypothesis = complete_code(input_text)
        scores_1gram.append(calculate_bleu(reference, hypothesis, 1))
        scores_2gram.append(calculate_bleu(reference, hypothesis, 2))
        scores_3gram.append(calculate_bleu(reference, hypothesis, 3))
        scores_4gram.append(calculate_bleu(reference, hypothesis, 4))

    average_1gram = np.mean(scores_1gram)
    average_2gram = np.mean(scores_2gram)
    average_3gram = np.mean(scores_3gram)
    average_4gram = np.mean(scores_4gram)

    return average_1gram, average_2gram, average_3gram, average_4gram

# test.json ファイルを読み込み
with open('test.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Evaluate model
average_1gram, average_2gram, average_3gram, average_4gram = evaluate_model(data)
print("Average 1-gram BLEU Score:", average_1gram)
print("Average 2-gram BLEU Score:", average_2gram)
print("Average 3-gram BLEU Score:", average_3gram)
print("Average 4-gram BLEU Score:", average_4gram)
