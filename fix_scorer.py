import re

with open('ESMO2025/E_composite_scorer.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'    EXPLAINABILITY_SCORES = \{.*?\n    \}'
replacement = """    EXPLAINABILITY_SCORES = {
        "Rules": 1.0,
        "REGLES": 1.0,  # Alias
        "FEUILLE NER À BASE DE RÈGLES": 1.0,
        "FEUILLE RÈGLES PAR DÉFAUT": 1.0,
        "ML_CRF": 0.7,
        "CRF": 0.7,
        "FEUILLE ML LÉGER NER": 0.7,
        "FEUILLE ML LÉGER PAR DÉFAUT": 0.7,
        "Transformer": 0.3,
        "BERT": 0.3,
        "FEUILLE NER TRANSFORMER BIDIRECTIONNEL": 0.3,
        "LLM": 0.1,
        "LLM_7B": 0.1,
        "LLM_API": 0.1,
        "FEUILLE NER LLM": 0.1,
    }"""

new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open('ESMO2025/E_composite_scorer.py', 'w', encoding='utf-8') as f:
    f.write(new_text)
print("CompositeScorer updated.")
