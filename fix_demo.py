import re

with open('ESMO2025/REST_interface/demo_rest.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"method": "REGLES"', '"method": "RÈGLES"')
text = text.replace('"method": "ML_NER"', '"method": "ML LÉGER"')

with open('ESMO2025/REST_interface/demo_rest.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated demo_rest.py mock.")
