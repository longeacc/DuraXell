#!/usr/bin/env python3
"""
Predict NER on .txt files and write BRAT .ann files.

Usage:
  python src/predict_to_brat.py \
      --model_dir "src/duraxell/NER/models/sweeps/DrBERT-7GB_lr2e-05_bs16_ep10_wd0.01_wr0.1_frz0_sd42" \
      --input_dir "src/duraxell/Breast/RCP/evaluation_set_breast_cancer" \
      --out_dir "src/duraxell/Breast/RCP/evaluation_set_breast_cancer_pred_ner" \
      --min_prob 0.0 --stride 50 --max_length 512
"""

import argparse
import json
import os

import numpy as np
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


# ---------- model resolution ----------
def resolve_model_dir(base_dir: str) -> str:
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
    cks = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if d.startswith("checkpoint-")
    ]
    cks = [d for d in cks if os.path.exists(os.path.join(d, "config.json"))]
    if cks:
        cks.sort(key=lambda p: int(p.rsplit("-", 1)[-1]))
        return cks[-1]
    raise FileNotFoundError(f"No valid HF model found under: {base_dir}")


def label_lookup(id2label, i: int) -> str:
    if isinstance(id2label, dict):
        if i in id2label:
            return id2label[i]
        s = str(i)
        if s in id2label:
            return id2label[s]
        for k, v in id2label.items():
            try:
                if int(k) == i:
                    return v
            except Exception:
                pass
        return "O"
    try:
        return id2label[i]
    except Exception:
        return "O"


# ---------- span utilities ----------
def merge_adjacent(spans: list[dict]) -> list[dict]:
    """Merge overlapping/contiguous spans of the same label."""
    if not spans:
        return []
    spans = sorted(spans, key=lambda x: (x["start"], x["end"], x["label"]))
    merged = [spans[0]]
    for s in spans[1:]:
        m = merged[-1]
        if s["label"] == m["label"] and s["start"] <= m["end"]:
            # overlap/adjacent → extend; avg prob weighted by length
            len_m = max(1, m["end"] - m["start"])
            len_s = max(1, s["end"] - s["start"])
            m["end"] = max(m["end"], s["end"])
            m["prob"] = (m["prob"] * len_m + s["prob"] * len_s) / (len_m + len_s)
        else:
            merged.append(s)
    return merged


def spans_from_chunk(pred_ids, probs, offsets, id2label, min_prob: float):
    spans = []
    cur = None
    cur_probs = []

    for pid, (s, e), pvec in zip(pred_ids, offsets, probs, strict=False):
        if s == e:  # special tokens
            continue

        tag = label_lookup(id2label, pid)
        # close current on 'O' or malformed tag
        if tag == "O" or "-" not in tag:
            if cur:
                cur["prob"] = float(np.mean(cur_probs)) if cur_probs else 0.0
                if cur["prob"] >= min_prob:
                    spans.append(cur)
            cur, cur_probs = None, []
            continue

        pref, ent = tag.split("-", 1)

        # start a new span if:
        #  - tag is B-
        #  - no current span exists (orphan I-)
        #  - entity type changed
        #  - there is a gap (new token starts after current end)
        start_new = (
            (pref == "B") or (cur is None) or (cur["label"] != ent) or (s > cur["end"])
        )

        if start_new:
            if cur:
                cur["prob"] = float(np.mean(cur_probs)) if cur_probs else 0.0
                if cur["prob"] >= min_prob:
                    spans.append(cur)
            cur = {"label": ent, "start": s, "end": e}
            cur_probs = [float(pvec[pid])]
        else:
            # continuation (I- of same entity without gap)
            cur["end"] = e
            cur_probs.append(float(pvec[pid]))

    if cur:
        cur["prob"] = float(np.mean(cur_probs)) if cur_probs else 0.0
        if cur["prob"] >= min_prob:
            spans.append(cur)
    return spans


# ---------- main prediction ----------
def predict_text(
    text: str,
    tok,
    model,
    max_length: int,
    stride: int,
    min_prob: float,
    keep_labels: list[str] = None,
):
    enc = tok(
        text,
        return_offsets_mapping=True,
        truncation=True,
        max_length=max_length,
        stride=stride,
        return_overflowing_tokens=True,
        return_special_tokens_mask=True,
    )
    input_ids_list = enc["input_ids"]
    attn_masks_list = enc["attention_mask"]
    offsets_list = enc["offset_mapping"]  # list[list[(s,e)]]
    # Use logits per chunk
    spans_all = []
    id2label = model.config.id2label
    device = next(model.parameters()).device
    for input_ids, attn_mask, offsets in zip(
        input_ids_list, attn_masks_list, offsets_list, strict=False
    ):
        tens = {
            "input_ids": torch.tensor([input_ids], device=device),
            "attention_mask": torch.tensor([attn_mask], device=device),
        }
        # Some models want token_type_ids; add if tokenizer provided it
        if "token_type_ids" in enc:
            len(spans_all)  # not used, just to ensure consistent indexing
        with torch.no_grad():
            logits = model(**tens).logits[0]  # [seq, labels]
            probs = torch.softmax(logits, dim=-1).cpu().numpy()
            pred_ids = logits.argmax(-1).cpu().tolist()

        # Filter out special tokens by checking offsets (0,0)
        offsets_no_special = []
        pred_ids_no_special = []
        probs_no_special = []
        for pid, (s, e), p in zip(pred_ids, offsets, probs, strict=False):
            if s == 0 and e == 0:
                continue
            offsets_no_special.append((s, e))
            pred_ids_no_special.append(pid)
            probs_no_special.append(p)
        spans = spans_from_chunk(
            pred_ids_no_special,
            np.array(probs_no_special),
            offsets_no_special,
            id2label,
            min_prob,
        )
        spans_all.extend(spans)

    # Deduplicate & merge overlaps
    # Optionally filter by label list
    if keep_labels:
        keep = set(keep_labels)
        spans_all = [s for s in spans_all if s["label"] in keep]
    # merge per label
    spans_all = merge_adjacent(spans_all)
    # dedupe identical (start,end,label)
    seen = set()
    uniq = []
    for s in spans_all:
        key = (s["start"], s["end"], s["label"])
        if key not in seen:
            seen.add(key)
            uniq.append(s)
    return uniq


def write_brat(txt_path: str, spans: list[dict], out_ann: str, text: str):
    os.makedirs(os.path.dirname(out_ann), exist_ok=True)
    with open(out_ann, "w", encoding="utf-8") as f:
        for i, s in enumerate(
            sorted(spans, key=lambda x: (x["start"], x["end"])), start=1
        ):
            frag = text[s["start"] : s["end"]].replace("\n", " ").replace("\t", " ")
            f.write(f"T{i}\t{s['label']} {s['start']} {s['end']}\t{frag}\n")


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
    cks = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if d.startswith("checkpoint-")
    ]
    cks = [d for d in cks if os.path.exists(os.path.join(d, "config.json"))]
    if cks:
        cks.sort(key=lambda p: int(p.rsplit("-", 1)[-1]))
        return cks[-1]
    raise FileNotFoundError(f"No valid model found under: {base_dir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--model_dir", required=True, help="Run root, /best, or checkpoint-*"
    )
    ap.add_argument("--input_dir", required=True, help="Folder of .txt files")
    ap.add_argument(
        "--out_dir", required=True, help="Where to write .ann (mirrors structure)"
    )
    ap.add_argument("--max_length", type=int, default=512, help="Tokenizer max length")
    ap.add_argument(
        "--stride", type=int, default=50, help="Token overlap between windows"
    )
    ap.add_argument(
        "--min_prob", type=float, default=0.0, help="Min mean token prob to keep a span"
    )
    ap.add_argument(
        "--keep_labels",
        nargs="*",
        default=None,
        help="If set, only keep these label names",
    )
    ap.add_argument("--device", default="auto", choices=["auto", "gpu", "cuda"])
    args = ap.parse_args()

    model_path = resolve_model_dir(_resolve_model_dir(args.model_dir))
    tok = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    if args.device == "cuda" and torch.cuda.is_available():
        model.to("cuda")
    elif args.device == "cpu":
        model.to("cpu")
    else:
        model.to("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()

    # Walk input_dir
    n_files, n_spans = 0, 0
    for root, _, files in os.walk(args.input_dir):
        for fn in files:
            if not fn.lower().endswith(".txt"):
                continue
            n_files += 1
            in_txt = os.path.join(root, fn)
            rel = os.path.relpath(in_txt, args.input_dir)
            out_ann = os.path.join(args.out_dir, os.path.splitext(rel)[0] + ".ann")
            os.makedirs(os.path.dirname(out_ann), exist_ok=True)

            text = open(in_txt, encoding="utf-8", errors="replace").read()
            spans = predict_text(
                text=text,
                tok=tok,
                model=model,
                max_length=args.max_length,
                stride=args.stride,
                min_prob=args.min_prob,
                keep_labels=args.keep_labels,
            )
            write_brat(in_txt, spans, out_ann, text)
            n_spans += len(spans)
            print(f"[OK] {rel}: {len(spans)} spans → {os.path.relpath(out_ann)}")
    print(f"\nDone. Files: {n_files}, total spans: {n_spans}")


if __name__ == "__main__":
    main()

try:
    t = globals().get('tracker'); t and t.stop()
except Exception as e:
    print(
        f"\nWarning: Generalized error in Eco2AI tracking (likely 'N/A' vs float dtype issue): {e}"
    )
    print(
        "Carbon emission tracking data could not be saved, but analysis results are preserved."
    )
