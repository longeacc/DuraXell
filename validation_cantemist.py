import glob
import pycrfsuite

def features(seq, i):
    word = seq[i][0]
    return {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'BOS': i == 0,
        'EOS': i == len(seq) - 1,
    }

def sent2features(seq):
    return [features(seq, i) for i in range(len(seq))]

print("Loading CRF model...")
tagger = pycrfsuite.Tagger()
tagger.open('crf_model.crfsuite')

cantemist_files = glob.glob('ESMO2025/REST_interface/cantemist-fr/cantemist-fr/*.txt')[:5]
print(f"\nEvaluating on {len(cantemist_files)} CANTEMIST-FR documents...")

for filepath in cantemist_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Tokenize roughly
    words = [w for w in text.replace('\\n', ' ').split(' ') if w.strip()]
    seq = [[w] for w in words]
    if not seq: continue
    
    X = sent2features(seq)
    y_pred = tagger.tag(X)
    
    extracted = []
    current_entity = []
    current_label = None
    
    for word, label in zip(words, y_pred):
        if label != 'O':
            if label.startswith('B-'):
                if current_entity:
                    extracted.append((current_label, " ".join(current_entity)))
                current_entity = [word]
                current_label = label[2:]
            elif label.startswith('I-'):
                current_entity.append(word)
        else:
            if current_entity:
                extracted.append((current_label, " ".join(current_entity)))
                current_entity = []
                current_label = None
                
    if current_entity:
        extracted.append((current_label, " ".join(current_entity)))
        
    print(f"\\nDoc: {filepath}")
    print(f"Text preview: {text[:100]}...")
    if extracted:
        # Group by label
        from collections import defaultdict
        grouped = defaultdict(list)
        for lbl, ent in extracted:
            grouped[lbl].append(ent)
        for lbl, ents in grouped.items():
            print(f"  [{lbl}]: {', '.join(ents)}")
    else:
        print("  (Aucune entite trouvee)")
