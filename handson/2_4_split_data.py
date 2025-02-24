import json

def split_json_file(input_file, split_index=7500):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    train_data = data[:split_index]
    test_data = data[split_index:]

    return train_data, test_data

def save_data(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

input_file = '../datasets/finetune_data/pandas.json'
train_output_file = '../datasets/finetune_data/pandas_train.json'
test_output_file = '../datasets/finetune_data/pandas_test.json'

train_data, test_data = split_json_file(input_file)
save_data(train_data, train_output_file)
save_data(test_data, test_output_file)