import os

try:
    from transformers import AutoTokenizer
    print("Transformers loaded ok.")
except Exception as e:
    print("Error loading transformers:", e)
