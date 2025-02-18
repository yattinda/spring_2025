from transformers import RobertaTokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq
import torch
import json
from torch.utils.data import Dataset, DataLoader

class CodeCompletionDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=512):
        self.examples = []
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for pair in data:
                input_text, target_text = pair[1], pair[0]
                input_ids = tokenizer.encode(input_text, max_length=max_length, truncation=True, padding='max_length')
                target_ids = tokenizer.encode(target_text, max_length=max_length, truncation=True, padding='max_length')
                self.examples.append((input_ids, target_ids))

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        input_ids, target_ids = self.examples[idx]
        return {
            'input_ids': torch.tensor(input_ids),
            'labels': torch.tensor(target_ids)
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a code completion model.")
    parser.add_argument("file_path", type=str, help="Path to the dataset file.")
    args = parser.parse_args()

    tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
    model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-small')

    dataset = CodeCompletionDataset(args.file_path, tokenizer)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator
    )

    trainer.train()

    # モデルを保存する
    model.save_pretrained('./finetuned_codet5_model')
    tokenizer.save_pretrained('./finetuned_codet5_tokenizer')

