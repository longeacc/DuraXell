# src/train_hf_ner.py
#pip install "transformers>=4.41" datasets seqeval accelerate
from datasets import load_dataset, Dataset, DatasetDict
from transformers import (AutoTokenizer, AutoModelForTokenClassification,
                          DataCollatorForTokenClassification, TrainingArguments, Trainer, EarlyStoppingCallback)
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score
import os
from eco2ai import set_params, Tracker



MODEL_ID = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext"

def read_conll_file(file_path):
    """
    Reads a CoNLL formatted file and processes it into sentences and tags.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sentences = []
    tags = []
    current_sent = []
    current_tags = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_sent:
                sentences.append(current_sent)
                tags.append(current_tags)
                current_sent = []
                current_tags = []
        else:
            parts = line.split()
            if len(parts) >= 2:
                current_sent.append(parts[0])
                current_tags.append(parts[-1])
    
    # Add last sentence if exists
    if current_sent:
        sentences.append(current_sent)
        tags.append(current_tags)
        
    return {"tokens": sentences, "ner_tags_str": tags}

def load_conll_splits():
    # Use absolute paths or correct relative paths based on workspace root
    base_path = "ESMO2025/NER/data/conll"
    train_path = os.path.join(base_path, "train.conll")
    dev_path = os.path.join(base_path, "dev.conll")
    
    train_data = read_conll_file(train_path)
    dev_data = read_conll_file(dev_path)
    
    return DatasetDict({
        "train": Dataset.from_dict(train_data),
        "dev":   Dataset.from_dict(dev_data),
    })

def main():
    ds = load_conll_splits()
    # replace the labels line with this:
    labels = sorted({
        tag
        for split in ds
        for doc in ds[split]["ner_tags_str"]   # doc = list of tags for a sentence
        for tag in doc                         # tag = individual tag
    })

    label2id = {l:i for i,l in enumerate(labels)}
    id2label = {i:l for l,i in label2id.items()}

    tok = AutoTokenizer.from_pretrained(MODEL_ID)

    def encode_batch(ex):
        # ex["tokens"] est une liste de listes de tokens (batch)
        # ex["ner_tags_str"] est une liste de listes de tags (batch)
        enc = tok(ex["tokens"], is_split_into_words=True, truncation=True, padding=True, max_length=512)
        all_labs = []
        
        for i, tags in enumerate(ex["ner_tags_str"]):
            wid = enc.word_ids(batch_index=i)
            prev, labs = None, []
            for w in wid:
                if w is None: 
                    labs.append(-100)
                elif w != prev:
                    labs.append(label2id.get(tags[w], label2id.get("O", 0)))
                else:
                    labs.append(-100)
                prev = w
            all_labs.append(labs)
        
        enc["labels"] = all_labs
        return enc

    enc = ds.map(encode_batch, batched=True, batch_size=32, remove_columns=["tokens","ner_tags_str"])
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_ID, num_labels=len(labels), id2label=id2label, label2id=label2id
    )

    args = TrainingArguments(
        output_dir="ESMO2025/NER/models/output/bc_ner",
        learning_rate=3e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        gradient_accumulation_steps=2,
        num_train_epochs=10,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        seed=42,
        logging_steps=50,
        report_to="none",
    )
    data_collator = DataCollatorForTokenClassification(tok)

    def compute_metrics(p):
        preds = np.argmax(p.predictions, axis=2)
        y_true, y_pred = [], []
        for pred, lab in zip(preds, p.label_ids):
            t_seq, p_seq = [], []
            for p_i, l_i in zip(pred, lab):
                if l_i == -100: continue
                t_seq.append(id2label[l_i]); p_seq.append(id2label[p_i])
            y_true.append(t_seq); y_pred.append(p_seq)
        return {
            "precision": precision_score(y_true, y_pred),
            "recall":    recall_score(y_true, y_pred),
            "f1":        f1_score(y_true, y_pred),
        }

    trainer = Trainer(
        model=model, args=args,
        train_dataset=enc["train"], eval_dataset=enc["dev"],
        tokenizer=tok, data_collator=data_collator,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    # Light layer freezing for tiny data
    for name, p in model.named_parameters():
        if name.startswith(("bert.embeddings", "bert.encoder.layer.0", "bert.encoder.layer.1")):
            p.requires_grad = False
    trainer.train()
    for p in model.parameters(): p.requires_grad = True
    trainer.train(resume_from_checkpoint=True)

    print(trainer.evaluate(enc["dev"]))
    trainer.save_model("ESMO2025/NER/models/output/bc_ner/best")

if __name__ == "__main__":
    main()
try:
    tracker.stop()
except Exception as e:
    print(f"\nWarning: Generalized error in Eco2AI tracking (likely 'N/A' vs float dtype issue): {e}")
    print("Carbon emission tracking data could not be saved, but analysis results are preserved.")