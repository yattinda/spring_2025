import json
import os

# JSONファイルが保存されているディレクトリ
directory = '../datasets/finetune_data'

merged_data = []

# ディレクトリ内のすべてのJSONファイルを読み込んで結合
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
            # もしデータがリストであれば、リストの要素を結合
            if isinstance(data, list):
                merged_data.extend(data)
            else:
                merged_data.append(data)

# JSON文字列として保存する際に、リストの外側の括弧を除外
with open('../datasets/finetune_data/merged_data.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print('JSONファイルの結合が完了しました。')
