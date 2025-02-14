import os
import json
import random
import argparse

def create_dataset(correct_python_file):
    python_files = open(os.path.join('../datasets/correct_python_file', correct_python_file)).read().splitlines()

    input_data = []
    target_data = []

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if any(char.isdigit() for char in line):  # 数値が入っている行を除外
                        continue
                    if '#' in line:  # #が入っている行を除外
                        continue
                    tokens = line.strip().split()
                    if len(tokens) > 5:  # トークン数が5つ以下の行を除外
                        input_data.append(line.strip())

                        # ランダムにトークンを削除したターゲットデータを作成
                        num_tokens_to_remove = random.randint(1, len(tokens) // 2)  # 削除するトークンの数をランダムに決定
                        target_tokens = tokens[:-num_tokens_to_remove]  # 最後から削除
                        target_line = ' '.join(target_tokens)
                        target_data.append(target_line)
        except UnicodeDecodeError:
                print(f"Skipping file: {file_path} due to encoding error.")

    dataset = list(zip(input_data, target_data))
    try:
        name, _ = os.path.splitext(correct_python_file)
        with open(os.path.join('../datasets/finetune_data', f'{name}.json'), 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
    except UnicodeEncodeError as e:
        print(f"Skipping writing to dataset.json due to encoding error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ahi')
    parser.add_argument('correct_python_file', type=str)

    args = parser.parse_args()
    create_dataset(args.correct_python_file)