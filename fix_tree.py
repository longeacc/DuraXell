import re

with open('ESMO2025/E_creation_arbre_decision.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'(if HAS_ECO2AI:.*?)\n\s+tracker\.stop\(\)', r'\1\n        try:\n            tracker.stop()\n        except Exception:\n            pass', text)

with open('ESMO2025/E_creation_arbre_decision.py', 'w', encoding='utf-8') as f:
    f.write(text)
