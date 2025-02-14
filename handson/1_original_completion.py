from transformers import RobertaTokenizer, T5ForConditionalGeneration

tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-small')

def complete_code(input_text, max_length=50):
    input_ids = tokenizer(input_text, return_tensors='pt').input_ids
    outputs = model.generate(input_ids, max_length=max_length, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

input_text = \
"""
def add_a_b():
  return a +
"""
output_text = complete_code(input_text)
print("補完結果:\n", output_text)
