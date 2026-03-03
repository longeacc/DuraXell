import re

with open('ESMO2025/REST_interface/rest_decision_bridge.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'    def _normalize_method\(self, method: str\) -> str:.*?        return "UNKNOWN"'

replacement = """    def _normalize_method(self, method: str) -> str:
        \"\"\"Normalise et aligne les noms de méthodes de l'arbre global et de l'interface REST empirique.\"\"\"
        m = method.upper()
        if m in ["RULES", "REGLES"] or "RÈGLES" in m:
            return "REGLES"
        if m in ["ML", "ML_NER", "ML_CRF", "TRANSFORMER"] or "ML" in m or "TRANSFORMER" in m:
            return "ML"
        if "LLM" in m:
            return "LLM"
        return "UNKNOWN" """

new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open('ESMO2025/REST_interface/rest_decision_bridge.py', 'w', encoding='utf-8') as f:
    f.write(new_text)
print("Bridge updated.")
