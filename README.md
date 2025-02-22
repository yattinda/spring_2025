# 環境構築
venvを仮想環境として用います．
venv環境内に入ったのち，requirement.txtを仮想環境内にインストールしてください
[(参考)](https://qiita.com/overflowfl/items/1db8746b9831bb15e9b5)
```
python -m venv .venv
source .venv/bin/activate
```

# リポジトリ構造
```
|
|--datasets(データ置き場)
|    |--raw(自分で作成する)
|    |--correct_python_file(2_1の出力)
|    |--finetune_data(2_2, 2_3の出力，Fine-tuneに利用)
|--handson(実行部分)
|    |--finetuned_model(自分で作成．WanDBのresultを格納する)
|    |--1_original.py(何もしてないCodeT5でのコード補完)
|    |--2_1_extract_python_file.py(git cloneしたリポジトリから.pyファイルを収集)
|    |--2_2_create_dataset.py(行単位で，入力と正解がセットになったJSONデータセットを生成)
|    |--2_3_json_concat.py(各プロジェクトごとのデータセットの結合)
|    |--3_finetune.py
|    |--4_eval_bleu.py(BLEUの出力, 3-5分程度かかる)
|    |--4_eval_levenshtein.py(levenshteinの出力, 3-5分程度かかる)
```

# 流れ
1. datasets以下にrawというディレクトリを作成
1. rawディレクトリに入って好きなGitHubプロジェクトをクローン（Pythonを推奨・それ以外の言語をしたいときはコード変更が必須）
1. 2_1_extract_python_file.py, 2_2_create_dataset.pyをそれぞれ順に実行(データセットが作成される)
2. 3_finetune.pyを実行し，モデルとトークナイザを作成する
3. output_dirとtokenizer.save_pretrainedのファイルの中身をfinetuned_modelにコピーする（後述）
4. 4_eval_**.pyを実行しモデルの評価を行う


# 各ファイルの実行例（無記載の場合は引数不必要，下段はNumpyでの例）
## 1_original.py
## 2_1_extract_python_file.py
```
python3 2_1_extract_python_file.py ../datasets/raw/<プロジェクト名> -o  <プロジェクト名>.txt

python3 2_1_extract_python_file.py ../datasets/raw/Numpy -o  numpy.txt
```

## 2_2_create_dataset.py
```
python3 2_2_create_dataset.py <プロジェクト名>.txt

python3 2_2_create_dataset.py numpy.txt   
```
## 3_finetune.py
実行後にたくさんのファイルが生成される．その中で，3_finetune.py内で指定したoutput_dirとtokenizer.save_pretrainedのファイルの中身を丸ごと上記のリポジトリ構造で示したfinetuned_modelにコピーする
## 4_eval_bleu.py & 4_eval_levenshtein.py
7行目と8行目のモデル名を自分が評価したいモデルの名前に変更する（コード内コメントアウト参照）
##
