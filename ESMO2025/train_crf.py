import os
import glob
import pycrfsuite
import re
from pathlib import Path

def tokenize_with_spans(text):
    # simple regex tokenizer that yields (token, start, end)
    for match in re.finditer(r'\w+|[^\w\s]', text):
        yield match.group(), match.start(), match.end()

def parse_ann(ann_content):
    spans = []
    for line in ann_content.splitlines():
        if line.startswith('T'):
            parts = line.split('\t')
            if len(parts) >= 3:
                info = parts[1].split()
                if len(info) >= 3 and ';' not in parts[1]: # ignore discontinuous for simplicity
                    etype = info[0]
                    start = int(info[1])
                    end = int(info[-1])
                    spans.append((start, end, etype))
    return spans

def build_dataset(data_dir):
    data_dir = Path(data_dir)
    X = []
    y = []

    for txt_file in data_dir.glob("*.txt"):
        ann_file = txt_file.with_suffix(".ann")
        if not ann_file.exists():
            continue
        
        text = txt_file.read_text(encoding='utf-8')
        ann_content = ann_file.read_text(encoding='utf-8')
        spans = parse_ann(ann_content)
        
        tokens = list(tokenize_with_spans(text))
        labels = ['O'] * len(tokens)
        
        for start, end, etype in spans:
            for i, (tok, t_start, t_end) in enumerate(tokens):
                if t_start >= start and t_end <= end:
                    if labels[i] == 'O':
                        # First token of entity or just in it
                        if i == 0 or labels[i-1] == 'O' or labels[i-1].split('-')[-1] != etype:
                            labels[i] = f"B-{etype}"
                        else:
                            labels[i] = f"I-{etype}"
        
        x_seq = [word2features(tokens, i) for i in range(len(tokens))]
        X.append(x_seq)
        y.append(labels)
        
    return X, y

def word2features(sent, i):
    word = sent[i][0]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
    ]
    if i > 0:
        word1 = sent[i-1][0]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=' + str(word1.istitle()),
            '-1:word.isupper=' + str(word1.isupper()),
        ])
    else:
        features.append('BOS')
        
    if i < len(sent) - 1:
        word1 = sent[i+1][0]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=' + str(word1.istitle()),
            '+1:word.isupper=' + str(word1.isupper()),
        ])
    else:
        features.append('EOS')
                
    return features

def train_crf(train_dir, output_model="crf_model.crfsuite"):
    print(f"Loading data from {train_dir}...")
    X_train, y_train = build_dataset(train_dir)
    print(f"Loaded {len(X_train)} documents.")
    
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)
        
    trainer.set_params({
        'c1': 0.1,
        'c2': 0.01,
        'max_iterations': 50,
        'feature.possible_transitions': True
    })
    
    print(f"Training CRF model and saving to {output_model}...")
    trainer.train(output_model)
    print("Training complete.")

if __name__ == "__main__":
    train_dir = Path(__file__).parent.parent / "NER" / "data" / "Breast" / "train"
    out_model = Path(__file__).parent / "crf_model.crfsuite"
    train_crf(train_dir, str(out_model))
