# DuraXELL — Import Dependency Report

Generated: 2026-02-28

---

## PER-FILE ANALYSIS

---

### ROOT FILES

---

**FILE: main.py**
  IMPORTS_INTERNAL: `ESMO2025.cascade_orchestrator` (lazy, inside function)
  IMPORTS_EXTERNAL: `argparse`, `sys`, `os`, `subprocess`
  SUBPROCESS_CALLS: `ESMO2025/E_templeability.py`, `ESMO2025/E_homogeneity.py`, `ESMO2025/E_creation_arbre_decision.py`, `ESMO2025/visualize_decision_tree.py`, `ESMO2025/REST_interface/demo_rest.py`, `run_full_pipeline_report.py`
  IMPORTED_BY: *(none — entry point)*

**FILE: run_full_pipeline_report.py**
  IMPORTS_INTERNAL: `ESMO2025.E_composite_scorer`, `ESMO2025.cascade_orchestrator`, `ESMO2025.energy_tracker`, `ESMO2025.visualize_decision_tree`, `ESMO2025.sensitivity_analysis`, `ESMO2025.REST_interface.rest_annotator`, `ESMO2025.REST_interface.rest_evaluator`, `ESMO2025.REST_interface.rest_decision_bridge`
  IMPORTS_EXTERNAL: `sys`, `os`, `json`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `time`
  IMPORTED_BY: *(none — entry point, called via subprocess by main.py)*

**FILE: fix_trackers.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`, `pathlib`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: fix_trackers2.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`, `pathlib`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: fix_bridge.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: fix_demo.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: fix_orch.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: fix_scorer.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: fix_tree.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`
  IMPORTED_BY: *(none — one-shot fix script)*

**FILE: debug_freq.py**
  IMPORTS_INTERNAL: `ESMO2025.E_frequency`
  IMPORTS_EXTERNAL: *(none)*
  IMPORTED_BY: *(none — debug script)*

**FILE: create_notebook.py**
  IMPORTS_INTERNAL: *(none at import-time; references internal modules in generated notebook cells)*
  IMPORTS_EXTERNAL: `nbformat`
  IMPORTED_BY: *(none — utility script)*

**FILE: test_psutil.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `sys`, `psutil`
  IMPORTED_BY: *(none — utility script)*

**FILE: test_run.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `traceback`, `os`, `sys`
  IMPORTED_BY: *(none — utility script)*

**FILE: test_transformers.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `transformers`
  IMPORTED_BY: *(none — utility script)*

---

### ESMO2025/ (Core Package)

---

**FILE: ESMO2025/__init__.py**
  IMPORTS_INTERNAL: `.E_annotation_yield`, `.E_creation_arbre_decision`, `.E_frequency`, `.E_homogeneity`, `.E_risk_context`, `.E_templeability`, `.cascade_orchestrator`, `.E_composite_scorer`, `.energy_tracker`
  IMPORTS_EXTERNAL: *(none)*
  IMPORTED_BY: *(implicitly by any `from ESMO2025 import ...` statement)*

**FILE: ESMO2025/structs.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `dataclasses`, `typing`
  IMPORTED_BY: `ESMO2025/cascade_orchestrator.py`, `ESMO2025/Rules/src/Breast/rules_cascade_connector.py`, `NER/src/ner_cascade_connector.py`, `ESMO2025/tests/test_cascade.py`, `ESMO2025/tests/test_pipeline_integration.py`

**FILE: ESMO2025/cascade_orchestrator.py**
  IMPORTS_INTERNAL: `ESMO2025.structs`, `ESMO2025.Rules.src.Breast.rules_cascade_connector` *(try/except)*, `NER.src.ner_cascade_connector` *(try/except)*
  IMPORTS_EXTERNAL: `json`, `os`, `sys`, `time`, `typing`, `pandas`
  IMPORTED_BY: `ESMO2025/__init__.py`, `main.py`, `run_full_pipeline_report.py`, `ESMO2025/tests/test_cascade.py`, `ESMO2025/tests/test_pipeline_integration.py`

**FILE: ESMO2025/energy_tracker.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `random`, `time`, `contextlib`, `pandas`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `run_full_pipeline_report.py`, `ESMO2025/tests/test_cascade.py`, `ESMO2025/tests/test_energy_tracker.py`, `ESMO2025/tests/test_pipeline_integration.py`

**FILE: ESMO2025/graph_orchestrator.py**
  IMPORTS_INTERNAL: *(none — file is empty)*
  IMPORTS_EXTERNAL: *(none)*
  IMPORTED_BY: *(none)*

**FILE: ESMO2025/visualize_decision_tree.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `matplotlib`, `networkx`
  IMPORTED_BY: `run_full_pipeline_report.py`

**FILE: ESMO2025/sensitivity_analysis.py**
  IMPORTS_INTERNAL: `E_creation_arbre_decision` *(try/except, local script-style import)*
  IMPORTS_EXTERNAL: `copy`, `json`, `os`, `sys`, `pandas`
  IMPORTED_BY: `run_full_pipeline_report.py`

**FILE: ESMO2025/E_creation_arbre_decision.py**
  IMPORTS_INTERNAL: `E_annotation_yield` *(try/except, local script-style import)*
  IMPORTS_EXTERNAL: `csv`, `json`, `os`, `pathlib`, `typing`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `ESMO2025/sensitivity_analysis.py`, `ESMO2025/tests/test_decision_tree.py`

**FILE: ESMO2025/E_composite_scorer.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `math`, `matplotlib`, `numpy`, `pandas`
  IMPORTED_BY: `ESMO2025/__init__.py`, `run_full_pipeline_report.py`, `ESMO2025/tests/test_composite_scorer.py`, `ESMO2025/tests/test_pipeline_integration.py`

**FILE: ESMO2025/E_annotation_yield.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `collections`, `pathlib`, `typing`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `ESMO2025/E_creation_arbre_decision.py`, `ESMO2025/tests/test_annotation_yield.py`

**FILE: ESMO2025/E_fesability_NER.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `csv`, `json`, `collections`, `pathlib`, `eco2ai` *(try/except)*
  IMPORTED_BY: *(none — standalone script)*

**FILE: ESMO2025/E_frequency.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `csv`, `math`, `collections`, `pathlib`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `debug_freq.py`, `ESMO2025/tests/test_frequency.py`

**FILE: ESMO2025/E_homogeneity.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `csv`, `json`, `math`, `re`, `collections`, `pathlib`, `typing`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `ESMO2025/tests/test_homogeneity.py`

**FILE: ESMO2025/E_risk_context.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `csv`, `re`, `collections`, `pathlib`, `typing`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `ESMO2025/tests/test_risk_context.py`

**FILE: ESMO2025/E_templeability.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `csv`, `json`, `math`, `os`, `re`, `collections`, `dataclasses`, `pathlib`, `typing`, `eco2ai` *(try/except)*
  IMPORTED_BY: `ESMO2025/__init__.py`, `ESMO2025/tests/test_templeability.py`

**FILE: ESMO2025/generate_homogeneity_report.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `csv`, `os`, `pathlib`, `eco2ai` *(hard import — will crash without eco2ai)*
  IMPORTED_BY: *(none — standalone script)*

**FILE: ESMO2025/generate_risk_context_report.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `csv`, `json`, `pathlib`, `eco2ai` *(hard import — will crash without eco2ai)*
  IMPORTED_BY: *(none — standalone script)*

**FILE: ESMO2025/generate_templeability_report.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `pathlib`, `eco2ai` *(hard import — will crash without eco2ai)*
  IMPORTED_BY: *(none — standalone script)*

---

### ESMO2025/REST_interface/

---

**FILE: ESMO2025/REST_interface/__init__.py**
  IMPORTS_INTERNAL: `convergence_analyzer`, `rest_annotator`, `rest_decision_bridge`, `rest_evaluator` *(relative script-style imports)*
  IMPORTS_EXTERNAL: *(none)*
  IMPORTED_BY: *(implicitly by any `from ESMO2025.REST_interface import ...`)*

**FILE: ESMO2025/REST_interface/rest_pipeline.py**
  IMPORTS_INTERNAL: `ESMO2025.REST_interface.rest_annotator`, `ESMO2025.REST_interface.rest_evaluator`, `ESMO2025.REST_interface.rest_decision_bridge`, `ESMO2025.REST_interface.yield_calculator`
  IMPORTS_EXTERNAL: `sys`, `os`
  IMPORTED_BY: *(none — entry point)*

**FILE: ESMO2025/REST_interface/rest_annotator.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `os`, `re`, `time`, `datetime`, `typing`
  IMPORTED_BY: `ESMO2025/REST_interface/__init__.py`, `ESMO2025/REST_interface/rest_pipeline.py`, `ESMO2025/REST_interface/demo_rest.py`, `run_full_pipeline_report.py`

**FILE: ESMO2025/REST_interface/rest_decision_bridge.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `os`
  IMPORTED_BY: `ESMO2025/REST_interface/__init__.py`, `ESMO2025/REST_interface/rest_pipeline.py`, `ESMO2025/REST_interface/demo_rest.py`, `run_full_pipeline_report.py`

**FILE: ESMO2025/REST_interface/rest_evaluator.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `math`, `os`
  IMPORTED_BY: `ESMO2025/REST_interface/__init__.py`, `ESMO2025/REST_interface/rest_pipeline.py`, `ESMO2025/REST_interface/demo_rest.py`, `run_full_pipeline_report.py`

**FILE: ESMO2025/REST_interface/demo_rest.py**
  IMPORTS_INTERNAL: `ESMO2025.REST_interface.convergence_analyzer`, `ESMO2025.REST_interface.rest_annotator`, `ESMO2025.REST_interface.rest_decision_bridge`, `ESMO2025.REST_interface.rest_evaluator`
  IMPORTS_EXTERNAL: `json`, `os`, `sys`, `time`
  IMPORTED_BY: *(none — entry point, called via subprocess by main.py)*

**FILE: ESMO2025/REST_interface/convergence_analyzer.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `matplotlib`
  IMPORTED_BY: `ESMO2025/REST_interface/__init__.py`, `ESMO2025/REST_interface/demo_rest.py`

**FILE: ESMO2025/REST_interface/yield_calculator.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `time`
  IMPORTED_BY: `ESMO2025/REST_interface/rest_pipeline.py`

---

### ESMO2025/REST_interface/REST_modules/

---

**FILE: REST_modules/__init__.py**
  IMPORTS_INTERNAL: `.categorization`, `.initialization`, `.loading`, `.ui`, `.visualization`
  IMPORTED_BY: *(parent package init)*

**FILE: REST_modules/categorization.py**
  IMPORTS_INTERNAL: `.calculs` *(star)*, `.extraction.normalisation` *(getEnt)*
  IMPORTS_EXTERNAL: `ipywidgets`, `pandas`
  IMPORTED_BY: `REST_modules/__init__.py`, `REST_modules/loading.py`, `REST_modules/ui.py`

**FILE: REST_modules/initialization.py**
  IMPORTS_INTERNAL: `.extraction.normalisation` *(getCat, getEnt)*
  IMPORTS_EXTERNAL: `ipywidgets`, `pandas`
  IMPORTED_BY: `REST_modules/__init__.py`, `REST_modules/ui.py`

**FILE: REST_modules/loading.py**
  IMPORTS_INTERNAL: `.calculs` *(star)*, `.categorization` *(create_ban_words_tfidf)*, `.extraction` *(star)*
  IMPORTS_EXTERNAL: `pandas` *(implicit)*
  IMPORTED_BY: `REST_modules/__init__.py`, `REST_modules/ui.py`

**FILE: REST_modules/ui.py**
  IMPORTS_INTERNAL: `.calculs`, `.categorization`, `.extraction`, `.initialization`, `.loading`, `.visualization`
  IMPORTS_EXTERNAL: `copy`, `math`, `os`, `ipywidgets`, `matplotlib`, `nltk`, `pandas`, `plotly`, `bqplot`, `ipydatagrid`, `ipyfilechooser`, `IPython`, `unidecode`
  IMPORTED_BY: `REST_modules/__init__.py`

**FILE: REST_modules/visualization.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `copy`, `pandas`, `plotly`, `bqplot`, `ipydatagrid`
  IMPORTED_BY: `REST_modules/__init__.py`, `REST_modules/ui.py`

**FILE: REST_modules/calculs/__init__.py**
  IMPORTS_INTERNAL: `.bootstrap`, `.concordancer`, `.metrics`, `.ngram`, `.recommendations`, `.regex`, `.results`, `.tfidf`
  IMPORTED_BY: `REST_modules/categorization.py`, `REST_modules/loading.py`, `REST_modules/ui.py`

**FILE: REST_modules/calculs/bootstrap.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `math`, `random`, `numpy`, `pandas`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`

**FILE: REST_modules/calculs/concordancer.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `re`, `pandas`, `ipydatagrid`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`

**FILE: REST_modules/calculs/metrics.py**
  IMPORTS_INTERNAL: `.regex` *(star import)*
  IMPORTS_EXTERNAL: `os`, `re`, `numpy`, `pandas`, `bqplot`, `ipydatagrid`, `unidecode`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`

**FILE: REST_modules/calculs/ngram.py**
  IMPORTS_INTERNAL: `.tfidf` *(attribution_tf)*
  IMPORTS_EXTERNAL: `nltk`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`

**FILE: REST_modules/calculs/recommendations.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `random`, `re`, `ipywidgets`, `matplotlib`, `numpy`, `pandas`, `seaborn`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`

**FILE: REST_modules/calculs/regex.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `re`, `inflect`, `unidecode`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`, `REST_modules/calculs/metrics.py`

**FILE: REST_modules/calculs/results.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `math`, `random`, `re`, `pandas`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`

**FILE: REST_modules/calculs/tfidf.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `math`, `re`, `nltk`, `numpy`, `pandas`
  IMPORTED_BY: `REST_modules/calculs/__init__.py`, `REST_modules/calculs/ngram.py`

**FILE: REST_modules/extraction/__init__.py**
  IMPORTS_INTERNAL: `.brat`, `.normalisation`, `.saving`
  IMPORTED_BY: `REST_modules/loading.py`, `REST_modules/ui.py`

**FILE: REST_modules/extraction/brat.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `glob`, `os`, `random`, `re`, `collections`
  IMPORTED_BY: `REST_modules/extraction/__init__.py`

**FILE: REST_modules/extraction/normalisation.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `copy`, `glob`, `json`, `os`, `re`, `pandas`, `spacy`, `Levenshtein`, `nltk`
  IMPORTED_BY: `REST_modules/extraction/__init__.py`, `REST_modules/categorization.py`, `REST_modules/initialization.py`

**FILE: REST_modules/extraction/saving.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `json`, `os`, `pandas`
  IMPORTED_BY: `REST_modules/extraction/__init__.py`

---

### ESMO2025/Rules/src/Breast/

---

**FILE: ESMO2025/Rules/src/Breast/rules_cascade_connector.py**
  IMPORTS_INTERNAL: `ESMO2025.Rules.src.Breast.biomarker_brat_annotator`, `ESMO2025.structs`
  IMPORTS_EXTERNAL: `os`, `sys`
  IMPORTED_BY: `ESMO2025/cascade_orchestrator.py` *(try/except)*

**FILE: ESMO2025/Rules/src/Breast/biomarker_brat_annotator.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `argparse`, `re`, `unicodedata`, `pathlib`, `typing`, `eco2ai` *(hard import)*
  IMPORTED_BY: `ESMO2025/Rules/src/Breast/rules_cascade_connector.py`, `ESMO2025/Rules/src/Breast/lunch.py`

**FILE: ESMO2025/Rules/src/Breast/lunch.py**
  IMPORTS_INTERNAL: `biomarker_brat_annotator` *(local/relative script-style import)*
  IMPORTS_EXTERNAL: `pprint`, `eco2ai` *(hard import)*
  IMPORTED_BY: *(none — standalone script)*

---

### ESMO2025/tests/

---

**FILE: ESMO2025/tests/conftest.py**
  IMPORTS_INTERNAL: *(none — mocks eco2ai via sys.modules)*
  IMPORTS_EXTERNAL: `sys`, `unittest.mock`
  IMPORTED_BY: *(pytest auto-loads)*

**FILE: ESMO2025/tests/test_annotation_yield.py**
  IMPORTS_INTERNAL: `ESMO2025.E_annotation_yield`
  IMPORTS_EXTERNAL: `sys`, `unittest.mock`, `pytest`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_cascade.py**
  IMPORTS_INTERNAL: `ESMO2025.structs`, `ESMO2025.cascade_orchestrator`, `ESMO2025.energy_tracker`
  IMPORTS_EXTERNAL: `sys`, `os`, `unittest.mock`, `pandas`, `pytest`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_composite_scorer.py**
  IMPORTS_INTERNAL: `ESMO2025.E_composite_scorer`
  IMPORTS_EXTERNAL: `pandas` *(in-body)*
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_decision_tree.py**
  IMPORTS_INTERNAL: `ESMO2025.E_creation_arbre_decision`
  IMPORTS_EXTERNAL: `sys`, `unittest.mock`, `pytest`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_energy_tracker.py**
  IMPORTS_INTERNAL: `ESMO2025.energy_tracker`
  IMPORTS_EXTERNAL: `pytest`, `os`, `pandas`, `unittest.mock`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_frequency.py**
  IMPORTS_INTERNAL: `ESMO2025.E_frequency`
  IMPORTS_EXTERNAL: `sys`, `unittest.mock`, `pytest`, `pathlib`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_homogeneity.py**
  IMPORTS_INTERNAL: `E_homogeneity` *(local path-based)*
  IMPORTS_EXTERNAL: `pytest`, `sys`, `os`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_pipeline_integration.py**
  IMPORTS_INTERNAL: `ESMO2025.cascade_orchestrator`, `ESMO2025.energy_tracker`, `ESMO2025.E_composite_scorer`
  IMPORTS_EXTERNAL: `pytest`, `pandas`, `unittest.mock`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_risk_context.py**
  IMPORTS_INTERNAL: `E_risk_context` *(local path-based)*
  IMPORTS_EXTERNAL: `pytest`, `sys`, `os`
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_simple.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: *(none)*
  IMPORTED_BY: *(none — test)*

**FILE: ESMO2025/tests/test_templeability.py**
  IMPORTS_INTERNAL: `E_templeability` *(local path-based)*
  IMPORTS_EXTERNAL: `pytest`, `sys`, `os`
  IMPORTED_BY: *(none — test)*

---

### NER/src/

---

**FILE: NER/src/ner_cascade_connector.py**
  IMPORTS_INTERNAL: `ESMO2025.structs`
  IMPORTS_EXTERNAL: `sys`, `os`, `torch`, `json`, `logging`, `transformers`
  IMPORTED_BY: `ESMO2025/cascade_orchestrator.py` *(try/except)*

**FILE: NER/src/2bis_train_hf_ner.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `datasets`, `transformers`, `numpy`, `seqeval`, `os`, `eco2ai`
  IMPORTED_BY: *(none — standalone training script)*

**FILE: NER/src/2sweep_ner.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `argparse`, `itertools`, `json`, `csv`, `typing`, `datasets`, `transformers`, `numpy`, `seqeval`, `eco2ai`
  IMPORTED_BY: *(none — standalone sweep script)*

**FILE: NER/src/3infer.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `json`, `torch`, `transformers`, `eco2ai`
  IMPORTED_BY: *(none — standalone inference script)*

**FILE: NER/src/4predict_to_brat.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `re`, `json`, `argparse`, `sys`, `typing`, `torch`, `numpy`, `transformers`, `eco2ai`
  IMPORTED_BY: *(none — standalone prediction script)*

**FILE: NER/src/5evaluate_ner.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `pandas`, `os`, `glob`
  IMPORTED_BY: *(none — standalone evaluation script)*

**FILE: NER/src/eval_best_model.py**
  IMPORTS_INTERNAL: *(none)*
  IMPORTS_EXTERNAL: `os`, `json`, `numpy`, `transformers`, `datasets`, `seqeval`
  IMPORTED_BY: *(none — standalone evaluation script)*

---

## ANALYSIS SUMMARY

---

### 1. MAIN ENTRY POINTS (files executed directly)

| Entry Point | Type | Description |
|---|---|---|
| `main.py` | CLI hub | Central CLI dispatcher (`extract`, `metrics`, `tree`, `rest`, `evaluate`) |
| `run_full_pipeline_report.py` | Pipeline | Full evaluation pipeline with figures |
| `ESMO2025/REST_interface/demo_rest.py` | Demo | REST interface demonstration |
| `ESMO2025/REST_interface/rest_pipeline.py` | Pipeline | REST annotation pipeline driver |
| `ESMO2025/E_creation_arbre_decision.py` | Script | Decision tree builder (also importable) |
| `ESMO2025/E_templeability.py` | Script | Templeability scorer (also importable) |
| `ESMO2025/E_homogeneity.py` | Script | Homogeneity scorer (also importable) |
| `ESMO2025/E_risk_context.py` | Script | Risk context scorer (also importable) |
| `ESMO2025/E_frequency.py` | Script | Frequency scorer (also importable) |
| `ESMO2025/E_annotation_yield.py` | Script | Annotation yield scorer (also importable) |
| `ESMO2025/E_fesability_NER.py` | Script | NER feasibility calculator |
| `ESMO2025/generate_*_report.py` (×3) | Script | HTML report generators |
| `ESMO2025/Rules/src/Breast/lunch.py` | Script | Rule-based annotation runner |
| `NER/src/2bis_train_hf_ner.py` | Script | NER training |
| `NER/src/2sweep_ner.py` | Script | NER hyperparameter sweep |
| `NER/src/3infer.py` | Script | NER inference |
| `NER/src/4predict_to_brat.py` | Script | NER prediction to BRAT format |
| `NER/src/5evaluate_ner.py` | Script | NER evaluation |
| `NER/src/eval_best_model.py` | Script | Best model evaluation |

---

### 2. DEPENDENCY CLASSIFICATION

#### LEAF MODULES (imported by others, import no project-internal files)

These are the foundational modules with zero internal dependencies:

| Module | Imported By |
|---|---|
| `ESMO2025/structs.py` | `cascade_orchestrator`, `rules_cascade_connector`, `ner_cascade_connector`, tests |
| `ESMO2025/energy_tracker.py` | `__init__`, `run_full_pipeline_report`, tests |
| `ESMO2025/E_composite_scorer.py` | `__init__`, `run_full_pipeline_report`, tests |
| `ESMO2025/E_annotation_yield.py` | `__init__`, `E_creation_arbre_decision`, tests |
| `ESMO2025/E_frequency.py` | `__init__`, `debug_freq`, tests |
| `ESMO2025/E_homogeneity.py` | `__init__`, tests |
| `ESMO2025/E_risk_context.py` | `__init__`, tests |
| `ESMO2025/E_templeability.py` | `__init__`, tests |
| `ESMO2025/visualize_decision_tree.py` | `run_full_pipeline_report` |
| `ESMO2025/REST_interface/rest_annotator.py` | `__init__`, `rest_pipeline`, `demo_rest`, `run_full_pipeline_report` |
| `ESMO2025/REST_interface/rest_evaluator.py` | `__init__`, `rest_pipeline`, `demo_rest`, `run_full_pipeline_report` |
| `ESMO2025/REST_interface/rest_decision_bridge.py` | `__init__`, `rest_pipeline`, `demo_rest`, `run_full_pipeline_report` |
| `ESMO2025/REST_interface/convergence_analyzer.py` | `__init__`, `demo_rest` |
| `ESMO2025/REST_interface/yield_calculator.py` | `rest_pipeline` |
| `ESMO2025/Rules/src/Breast/biomarker_brat_annotator.py` | `rules_cascade_connector`, `lunch.py` |
| All `REST_modules/calculs/*.py` | via `calculs/__init__` |
| All `REST_modules/extraction/*.py` | via `extraction/__init__` |
| `REST_modules/visualization.py` | `__init__`, `ui.py` |

#### ROOT MODULES (import other project files, never imported by anyone)

These are the top-level entry points or standalone scripts:

| Module | Depends On |
|---|---|
| `main.py` | `cascade_orchestrator` (+ subprocess calls to many scripts) |
| `run_full_pipeline_report.py` | `E_composite_scorer`, `cascade_orchestrator`, `energy_tracker`, `visualize_decision_tree`, `sensitivity_analysis`, REST interface modules |
| `ESMO2025/REST_interface/demo_rest.py` | REST interface modules |
| `ESMO2025/REST_interface/rest_pipeline.py` | REST interface modules + `yield_calculator` |
| `ESMO2025/Rules/src/Breast/lunch.py` | `biomarker_brat_annotator` |
| `debug_freq.py` | `E_frequency` |
| All `ESMO2025/tests/*.py` | Various ESMO2025 modules |
| All `NER/src/*.py` (except `ner_cascade_connector`) | External only |

#### HUB MODULES (both imported and import others)

| Module | Imports | Imported By |
|---|---|---|
| `ESMO2025/__init__.py` | 9 internal modules | All external `ESMO2025.*` imports |
| `ESMO2025/cascade_orchestrator.py` | `structs`, `rules_cascade_connector`, `ner_cascade_connector` | `__init__`, `main`, `run_full_pipeline_report`, tests |
| `ESMO2025/E_creation_arbre_decision.py` | `E_annotation_yield` | `__init__`, `sensitivity_analysis`, tests |
| `ESMO2025/sensitivity_analysis.py` | `E_creation_arbre_decision` | `run_full_pipeline_report` |
| `ESMO2025/Rules/src/Breast/rules_cascade_connector.py` | `biomarker_brat_annotator`, `structs` | `cascade_orchestrator` |
| `NER/src/ner_cascade_connector.py` | `structs` | `cascade_orchestrator` |
| `REST_modules/ui.py` | all other REST_modules | `__init__` |
| `REST_modules/loading.py` | `calculs`, `categorization`, `extraction` | `__init__`, `ui` |
| `REST_modules/categorization.py` | `calculs`, `extraction.normalisation` | `__init__`, `loading`, `ui` |
| `REST_modules/calculs/metrics.py` | `.regex` | `calculs/__init__` |
| `REST_modules/calculs/ngram.py` | `.tfidf` | `calculs/__init__` |

---

### 3. CIRCULAR DEPENDENCY ANALYSIS

**No true circular import dependencies found.**

The closest potential issue:
- `ESMO2025/__init__.py` imports `cascade_orchestrator`, which imports `rules_cascade_connector`, which imports `ESMO2025.structs`. But `structs` is loaded first by `__init__.py` order, so there's no cycle.
- `ESMO2025/__init__.py` imports both `E_creation_arbre_decision` and `E_annotation_yield`. `E_creation_arbre_decision` also imports `E_annotation_yield`, but this is a DAG, not a cycle.
- `REST_modules/__init__.py` → `categorization` → `.calculs` → (submodules). No back-references.

**All dependency graphs are DAGs (Directed Acyclic Graphs). No circular imports exist.**

---

### 4. CORE DEPENDENCY CHAIN (Main Pipeline)

```
main.py
  └── cascade_orchestrator.py
        ├── structs.py                    [LEAF]
        ├── rules_cascade_connector.py
        │     ├── biomarker_brat_annotator.py  [LEAF]
        │     └── structs.py                    [LEAF]
        └── ner_cascade_connector.py
              └── structs.py                    [LEAF]

run_full_pipeline_report.py
  ├── E_composite_scorer.py               [LEAF]
  ├── cascade_orchestrator.py             (see above)
  ├── energy_tracker.py                   [LEAF]
  ├── visualize_decision_tree.py          [LEAF]
  ├── sensitivity_analysis.py
  │     └── E_creation_arbre_decision.py
  │           └── E_annotation_yield.py   [LEAF]
  ├── rest_annotator.py                   [LEAF]
  ├── rest_evaluator.py                   [LEAF]
  └── rest_decision_bridge.py             [LEAF]
```

---

### 5. EXTERNAL DEPENDENCY SUMMARY

| Library | Used By (count) | Category |
|---|---|---|
| `pandas` | 15+ files | Data manipulation |
| `matplotlib` | 8+ files | Visualization |
| `numpy` | 7+ files | Numerics |
| `eco2ai` | 13 files | Energy tracking |
| `json` (stdlib) | 15+ files | Config/serialization |
| `re` (stdlib) | 12+ files | Regex |
| `torch` | 3 files (NER) | Deep learning |
| `transformers` | 5 files (NER) | HuggingFace models |
| `seqeval` | 3 files (NER) | NER evaluation |
| `datasets` | 3 files (NER) | HuggingFace datasets |
| `networkx` | 1 file | Graph visualization |
| `seaborn` | 2 files | Statistical plots |
| `ipywidgets` | 4 files (REST_modules) | Jupyter UI |
| `bqplot` | 3 files (REST_modules) | Jupyter plots |
| `ipydatagrid` | 4 files (REST_modules) | Jupyter tables |
| `plotly` | 2 files (REST_modules) | Interactive plots |
| `spacy` | 1 file (normalisation) | NLP |
| `Levenshtein` | 1 file (normalisation) | String distance |
| `inflect` | 1 file (regex) | Pluralization |
| `nltk` | 3 files (REST_modules) | NLP toolkit |
| `nbformat` | 1 file | Notebook creation |
| `psutil` | 1 file | Process monitoring |
| `unidecode` | 3 files (REST_modules) | Unicode normalization |

---

### 6. WARNINGS & OBSERVATIONS

1. **Hard eco2ai imports** in `generate_*_report.py` (×3) and `biomarker_brat_annotator.py` and `lunch.py` — these will crash if `eco2ai` is not installed (no try/except guard).

2. **Inconsistent import styles** in tests: `test_homogeneity.py`, `test_risk_context.py`, and `test_templeability.py` use `sys.path.append` + bare module imports (`from E_homogeneity import ...`) instead of package-qualified imports (`from ESMO2025.E_homogeneity import ...`).

3. **REST_interface/__init__.py** uses bare module imports (`from convergence_analyzer import ...`) instead of relative imports (`from .convergence_analyzer import ...`), which will fail when imported as a package from outside the directory.

4. **graph_orchestrator.py** is an empty file — appears to be a placeholder.

5. **E_fesability_NER.py** is a standalone script not imported by any other file.

6. **NER/src/** pipeline scripts (2bis, 2sweep, 3infer, 4predict, 5evaluate, eval_best) are fully standalone — they have no internal project imports and are never imported by others. Only `ner_cascade_connector.py` bridges into the main DuraXELL system.
