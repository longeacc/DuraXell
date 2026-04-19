import sys
import os
import torch
import logging
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Ensure imports work from project root (assuming standard placement)
# Expected structure: root/NER/src/ner_cascade_connector.py
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)  # Go up to DuraXELL root

try:
    from duraxell.structs import ExtractionResult
except ImportError:
    # Fallback if path is weird
    from structs import ExtractionResult


class NERCascadeConnector:
    """
    Connecteur pour le modèle NER Transformer (DrBERT fine-tuné).
    Charge le modèle une fois à l'init.
    """

    def __init__(self, model_dir: str = None, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None

        if not model_dir:
            # Attempt to auto-discover best model
            base_models_dir = os.path.join(
                os.path.dirname(__file__), "../models/sweeps"
            )
            if os.path.exists(base_models_dir):
                candidates = [
                    os.path.join(base_models_dir, d)
                    for d in os.listdir(base_models_dir)
                ]
                candidates = [d for d in candidates if os.path.isdir(d)]
                if candidates:
                    # Pick most recent
                    model_dir = max(candidates, key=os.path.getmtime)

        self.model_dir = model_dir

        if self.model_dir and os.path.exists(self.model_dir):
            try:
                self._load_model()
            except Exception as e:
                logging.warning(f"Failed to load NER model from {self.model_dir}: {e}")
        else:
            logging.warning(f"NER model directory not found or empty: {self.model_dir}")

    def _load_model(self):
        # Locate effective checkpoint directory (often inside the sweep dir)
        # Logic adapted from 3infer.py
        effective_dir = self.model_dir

        # Check if direct config exists
        if not os.path.exists(os.path.join(effective_dir, "config.json")):
            # Look for checkpoint-* subfolders
            subdirs = [
                os.path.join(self.model_dir, d)
                for d in os.listdir(self.model_dir)
                if d.startswith("checkpoint-")
            ]
            if subdirs:
                # Pick last checkpoint by number
                subdirs.sort(key=lambda x: int(x.split("-")[-1]))
                effective_dir = subdirs[-1]

        logging.info(f"Loading NER model from {effective_dir} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(effective_dir, use_fast=True)
        self.model = AutoModelForTokenClassification.from_pretrained(effective_dir).to(
            self.device
        )
        self.model.eval()

    def predict(self, text: str, entity_type: str) -> ExtractionResult:
        """
        Exécute l'inférence NER sur le texte.
        Retourne le span correspondant à l'entité demandée avec la confiance max.
        """
        if not self.model or not self.tokenizer:
            # Fallback mock if model failed to load
            return ExtractionResult(
                entity_type, None, "Transformer (Mock)", 0.0, 0.0, 2
            )

        # 1. Tokenize (max_length=512 to avoid BERT overflow on long clinical docs)
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            return_offsets_mapping=True,
        ).to(self.device)
        offsets = inputs.pop("offset_mapping")[0].cpu().tolist()

        # 2. Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits[0]  # (seq_len, num_labels)
            probs = torch.softmax(logits, dim=-1)
            pred_ids = logits.argmax(-1).cpu().tolist()

        # 3. Decode entities
        id2label = self.model.config.id2label
        entities_found = []

        current_entity = None

        for idx, (label_id, (start, end)) in enumerate(zip(pred_ids, offsets)):
            if start == end:
                continue  # Special tokens

            label = id2label[label_id]
            conf = probs[idx][label_id].item()

            if label == "O":
                if current_entity:
                    entities_found.append(current_entity)
                    current_entity = None
                continue

            # B-ENTITY or I-ENTITY
            prefix, tag = label.split("-", 1) if "-" in label else ("", label)

            if prefix == "B" or (current_entity and current_entity["type"] != tag):
                if current_entity:
                    entities_found.append(current_entity)
                current_entity = {
                    "type": tag,
                    "start": start,
                    "end": end,
                    "text": text[start:end],
                    "confidence": conf,
                    "conf_sum": conf,
                    "tokens": 1,
                }
            elif prefix == "I" and current_entity and current_entity["type"] == tag:
                current_entity["end"] = end
                current_entity["text"] += text[
                    current_entity["end_prev"] : end
                ]  # Handle spaces if any? Actually slice from orig text is better
                # Logic update: just update end, text will be sliced at end
                current_entity["conf_sum"] += conf
                current_entity["tokens"] += 1

            if current_entity:
                current_entity["end_prev"] = end  # marker

        if current_entity:
            entities_found.append(current_entity)

        # 4. Filter for requested entity input
        # Map DuraXELL entity to Model entity (e.g. "Estrogen_receptor" -> "ER"?)
        # Let's assume naive mapping or direct match for now.
        # Check what labels model uses. Usually "HER2", "ER" etc.

        # Heuristic mapping
        target_tags = [entity_type]
        if entity_type == "Estrogen_receptor":
            target_tags = ["ER", "Estrogen_Receptor"]
        if entity_type == "HER2":
            target_tags = ["HER2", "CerbB2"]

        best_match = None
        best_conf = -1.0

        for cand in entities_found:
            # Check if candidate type matches requested
            # Flexible matching
            if cand["type"] in target_tags or entity_type in cand["type"]:
                # Compute avg confidence
                avg_conf = cand["conf_sum"] / cand["tokens"]
                if avg_conf > best_conf:
                    best_conf = avg_conf
                    best_match = cand

        if best_match:
            # Extract clean text from original using start/end
            final_text = text[best_match["start"] : best_match["end"]]
            return ExtractionResult(
                entity_type=entity_type,
                value=final_text,
                method_used="Transformer",
                confidence=best_conf,
                energy_kwh=0.0,  # Filled by orchestrator
                cascade_level=2,
                span=(best_match["start"], best_match["end"]),
            )

        return ExtractionResult(entity_type, None, "Transformer", 0.0, 0.0, 2)
