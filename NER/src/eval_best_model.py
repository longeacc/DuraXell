import os

import numpy as np
from datasets import Dataset, DatasetDict
from seqeval.metrics import classification_report
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)


def read_conll(path):
    texts, labels = [], []
    with open(path, encoding="utf-8") as f:
        words, tags = [], []
        for line in f:
            line = line.strip()
            if not line:
                if words:
                    texts.append(words)
                    labels.append(tags)
                    words, tags = [], []
            else:
                parts = line.split()
                words.append(parts[0])
                tags.append(parts[-1])
        if words:
            texts.append(words)
            labels.append(tags)
    return texts, labels


def build_dataset(data_dir):
    test_t, test_y = read_conll(os.path.join(data_dir, "test.conll"))

    all_tags = set()
    for tags in test_y:
        all_tags.update(tags)
    label_list = sorted(list(all_tags))
    if "O" in label_list:
        label_list.remove("O")
        label_list.insert(0, "O")

    ds = DatasetDict({"test": Dataset.from_dict({"tokens": test_t, "ner_tags": test_y})})
    return ds, label_list


def encode_with_labels(ds, model_id, label2id):
    tok = AutoTokenizer.from_pretrained(model_id, add_prefix_space=True)

    def tokenize_and_align(examples):
        tokenized = tok(examples["tokens"], truncation=True, is_split_into_words=True)
        labels = []
        for i, label in enumerate(examples["ner_tags"]):
            word_ids = tokenized.word_ids(batch_index=i)
            prev_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx != prev_word_idx:
                    label_ids.append(label2id[label[word_idx]])
                else:
                    label_ids.append(-100)
                prev_word_idx = word_idx
            labels.append(label_ids)
        tokenized["labels"] = labels
        return tokenized

    enc = ds.map(tokenize_and_align, batched=True)
    return tok, enc, {v: k for k, v in label2id.items()}


def main():
    data_dir = "NER/data/conll"
    model_dir = "NER/models/sweeps/DrBERT-7GB_lr2e-05_bs16_ep5_wd0.0_wr0.1_frz0_sd42"

    if not os.path.exists(model_dir):
        print(f"Model directory {model_dir} not found.")
        return

    ds, label_list = build_dataset(data_dir)
    label2id = {lbl: i for i, lbl in enumerate(label_list)}

    tok, enc, id2label = encode_with_labels(ds, model_dir, label2id)

    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    data_collator = DataCollatorForTokenClassification(tok)

    training_args = TrainingArguments(
        output_dir="./tmp", per_device_eval_batch_size=4, report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        processing_class=tok,
        data_collator=data_collator,
    )

    predictions, labels, _ = trainer.predict(enc["test"])
    preds = np.argmax(predictions, axis=2)

    y_true, y_pred = [], []
    for pred, lab in zip(preds, labels, strict=False):
        t_seq, p_seq = [], []
        for p_i, l_i in zip(pred, lab, strict=False):
            if l_i == -100:
                continue
            t_seq.append(id2label[l_i])
            p_seq.append(id2label[p_i])
        y_true.append(t_seq)
        y_pred.append(p_seq)

    report = classification_report(y_true, y_pred, digits=4)
    print(report)


if __name__ == "__main__":
    main()
