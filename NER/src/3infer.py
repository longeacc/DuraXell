# src/infer.py
import os, json, torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from eco2ai import set_params, Tracker



def _resolve_model_dir(base_dir: str) -> str:
    cfg = os.path.join(base_dir, "config.json")
    if os.path.exists(cfg):
        try:
            if "model_type" in json.load(open(cfg)):
                return base_dir
        except Exception:
            pass
    state_path = os.path.join(base_dir, "trainer_state.json")
    if os.path.exists(state_path):
        best = json.load(open(state_path)).get("best_model_checkpoint")
        if best and os.path.exists(os.path.join(best, "config.json")):
            return best
    cks = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if d.startswith("checkpoint-")]
    cks = [d for d in cks if os.path.exists(os.path.join(d, "config.json"))]
    if cks:
        cks.sort(key=lambda p: int(p.rsplit("-", 1)[-1]))
        return cks[-1]
    raise FileNotFoundError(f"No valid model found under: {base_dir}")

def load_model(base_dir: str):
    mdir = _resolve_model_dir(base_dir)
    print(f"Loading model from: {mdir}")
    tok = AutoTokenizer.from_pretrained(mdir, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(mdir)
    model.eval()
    return tok, model

def _label_lookup(id2label, i: int) -> str:
    # supports dict with int or str keys, or list
    if isinstance(id2label, dict):
        if i in id2label:
            return id2label[i]
        s = str(i)
        if s in id2label:
            return id2label[s]
        # last resort: try to coerce keys
        for k, v in id2label.items():
            try:
                if int(k) == i:
                    return v
            except Exception:
                pass
        return "O"
    # list/tuple
    try:
        return id2label[i]
    except Exception:
        return "O"

def predict(text: str, model_dir: str):
    tok, model = load_model(model_dir)
    enc = tok(text, return_offsets_mapping=True, truncation=True, return_tensors="pt")
    inputs = {k: v for k, v in enc.items() if k in ("input_ids", "attention_mask", "token_type_ids")}
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    pred_ids = logits.argmax(-1).tolist()
    offsets  = enc["offset_mapping"][0].tolist()
    id2label = model.config.id2label

    spans, cur = [], None
    for lab_id, (s, e) in zip(pred_ids, offsets):
        if s == e:  # special tokens like CLS/SEP
            continue
        tag = _label_lookup(id2label, lab_id)
        if tag == "O" or "-" not in tag:
            if cur: spans.append(cur); cur = None
            continue
        prefix, ent = tag.split("-", 1)
        if prefix == "B" or (cur and cur["label"] != ent):
            if cur: spans.append(cur)
            cur = {"label": ent, "start": s, "end": e}
        else:
            cur["end"] = e
    if cur: spans.append(cur)
    return [{"text": text[s:e], **d} for d in spans]

if __name__ == "__main__":
    base_run_dir = "NER/models/sweeps/DrBERT-7GB_lr2e-05_bs16_ep10_wd0.01_wr0.1_frz2_sd42"
    sample = "HER2 3+ ER négatif ; PR positif. Ki-67 30%."
    print(predict(sample, base_run_dir))

try:
    tracker.stop()
except Exception as e:
    print(f"\nWarning: Generalized error in Eco2AI tracking (likely 'N/A' vs float dtype issue): {e}")
    print("Carbon emission tracking data could not be saved, but analysis results are preserved.")