import sys
from unittest.mock import MagicMock

sys.modules["eco2ai"] = MagicMock()

from ESMO2025.E_annotation_yield import AnnotationYieldScorer


def test_yield_metrics():
    scorer = AnnotationYieldScorer()

    # GS: 2 entities
    gs_content = """T1\tGene 0 5\tBRCA1
T2\tGene 10 15\tBRCA2"""

    # Pred: 1 match (TP), 1 FP, 1 FN
    # T1 matches GS T1 -> TP
    # GS T2 missing -> FN
    # T3 fake -> FP
    pred_content = """T1\tGene 0 5\tBRCA1
T3\tGene 20 25\tFake"""

    scorer.update_counts(gs_content, pred_content)

    scores = scorer.get_scores()
    gene_score = scores["Gene"]

    # Check counts
    assert scorer.tp["Gene"] == 1
    assert scorer.fn["Gene"] == 1
    assert scorer.fp["Gene"] == 1

    # Check Precision: TP / (TP+FP) = 1/2 = 0.5
    assert gene_score["Precision"] == 0.5

    # Check Recall: TP / (TP+FN) = 1/2 = 0.5
    assert gene_score["Recall"] == 0.5

    # Check F1: 2 * 0.5 * 0.5 / 1.0 = 0.5
    assert gene_score["F1-Yield"] == 0.5


def test_empty_yield():
    scorer = AnnotationYieldScorer()
    scorer.update_counts("", "")
    scores = scorer.get_scores()
    assert scores == {}


def test_disjoint_span():
    # T1 has span 0 5;10 15.
    # Our simple parser takes 0 and 15.
    gs_content = "T1\tGene 0 5;10 15\tComplex"
    pred_content = "T1\tGene 0 15\tComplex"

    # Parser strictness check
    scorer = AnnotationYieldScorer()
    # Mocking parser for exact match would depend on impl.
    # My impl: start=0, end=15.

    scorer.update_counts(gs_content, pred_content)
    # Both should parse as ("Gene", 0, 15)
    assert scorer.tp["Gene"] == 1

    gs_parsed = scorer._parse_ann_content(gs_content)
    assert ("Gene", 0, 15) in gs_parsed
