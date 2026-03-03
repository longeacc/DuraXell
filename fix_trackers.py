import re
from pathlib import Path

files = [
    "NER/src/1convert_brat_to_conll.py",
    "NER/src/2bis_train_hf_ner.py",
    "NER/src/2sweep_ner.py",
    "NER/src/3infer.py",
    "NER/src/4predict_to_brat.py"
]

for f in files:
    p = Path(f)
    if not p.exists(): continue
    text = p.read_text('utf-8')
    
    # We remove the global Tracker instantiation
    text = re.sub(r"tracker\s*=\s*Tracker\(\)\n?tracker\.start\(\)\n?", "", text)
    
    # We also remove the global eco2ai set_params blocks
    text = re.sub(r'set_params\(\s*project_name=[^)]+\n\)\n?', '', text)
    
    p.write_text(text, 'utf-8')
    print(f"Fixed {f}")
