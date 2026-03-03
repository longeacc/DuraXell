"""
Build and execute the DuraXELL Decision Tree.
Generates 'decision_config.json' and 'output_decision.txt'.

Decision Tree Logic (Priority Order):
1. Templeability (Te) & Homogeneity (He) (Structure) -> HIGH? -> RULES
2. Risk Context (R) -> HIGH? -> LLM / REVIEW
3. Frequency (Freq) & Annotation Yield -> RULES vs ML (NER) vs LLM

Outputs:
- decision_config.json: Machine-readable config for the orchestrator.
- output_decision.txt: Human-readable report.
"""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict

# Eco2AI tracking
try:
    from eco2ai import Tracker, set_params

    HAS_ECO2AI = True
except ImportError:
    HAS_ECO2AI = False

if __name__ == "__main__" and HAS_ECO2AI:
    set_params(
        project_name="Consumtion_of_E_creation_arbre_decision.py",
        experiment_description="Building Decision Tree Config",
        file_name="Consumtion_of_Duraxell.csv",
    )
    tracker = Tracker()
    tracker.start()

# Import metrics scorers (Assuming they are in same package or path)
try:
    # We try local imports if running as script in same dir
    from E_annotation_yield import AnnotationYieldScorer
except ImportError:
    try:
        from ESMO2025.E_annotation_yield import AnnotationYieldScorer
    except ImportError:
        try:
            from .E_annotation_yield import AnnotationYieldScorer
        except (ImportError, SystemError):
            pass


class DecisionTreeBuilder:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.decisions = {}

        # --- CALIBRATED THRESHOLDS (Based on Audit) ---
        self.THRESHOLDS = {
            "TE_HIGH": 70.0,
            "TE_MED": 40.0,
            "HE_HIGH": 70.0,
            "RISK_HIGH": 0.5,
            "FREQ_MIN": 0.001,
            "YIELD_HIGH": 0.75,
            "YIELD_MIN_RULES": 0.25,   # Minimum Yield for rules routing via noeud 1b
            "FEAS_NER": 0.6,
            "DOMAIN_SHIFT_MAX": 0.5,
            "LLM_NEC_HIGH": 0.5
        }

    # Nombre minimum d'occurrences pour que Te soit fiable (Aligné avec THRESHOLDS_JUSTIFICATION.md)
    MIN_TE_SAMPLES = 10

    def validate_thresholds_kfold(self, entities_metrics: Dict[str, Dict[str, float]], k: int = 5):
        """
        Validation croisée k-fold sur les seuils : partitionner le corpus en k plis,
        calibrer les seuils sur k-1 plis, mesurer la stabilité des décisions sur le pli restant.
        """
        import random
        
        entities = list(entities_metrics.keys())
        if len(entities) < k:
            print(f"Pas assez d'entités pour une CV {k}-fold.")
            return

        random.shuffle(entities)
        
        # Split en k plis
        folds = [entities[i::k] for i in range(k)]
        stabilities = []

        print(f"--- Début de la validation croisée {k}-fold des seuils ---")
        
        for i in range(k):
            test_entities = folds[i]
            train_entities = [ent for j, f in enumerate(folds) if j != i for ent in f]
            
            # Simulation d'une calibration : modification mineure d'un seuil basée sur le train set
            train_te_vals = sorted([entities_metrics[ent].get("Te", 0.0) for ent in train_entities])
            if train_te_vals:
                # 75e percentile manuel
                idx = int(len(train_te_vals) * 0.75)
                calibrated_te_med = train_te_vals[idx] if idx < len(train_te_vals) else self.THRESHOLDS["TE_MED"]
            else:
                calibrated_te_med = self.THRESHOLDS["TE_MED"]
            
            # Stocker l'ancien
            old_te_med = self.THRESHOLDS["TE_MED"]
            # Appliquer le seuil calibré
            self.THRESHOLDS["TE_MED"] = calibrated_te_med
            
            # Mesurer l'accord (stabilité) entre les règles par défaut et les calibrées
            matches = 0
            for ent in test_entities:
                metrics = entities_metrics[ent]
                # Modèle origine
                self.THRESHOLDS["TE_MED"] = old_te_med
                orig_decision = self.analyze_entity(ent, metrics).get("method", "")
                # Modèle calibré
                self.THRESHOLDS["TE_MED"] = calibrated_te_med
                new_decision = self.analyze_entity(ent, metrics).get("method", "")
                
                if orig_decision == new_decision:
                    matches += 1
                    
            stability = matches / max(1, len(test_entities))
            stabilities.append(stability)
            self.THRESHOLDS["TE_MED"] = old_te_med # Reset

        avg_stability = sum(stabilities) / len(stabilities)
        print(f"Stabilité moyenne des décisions (K-Fold, k={k}): {avg_stability:.2%}")

    def analyze_entity(self, entity: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Apply the recursive decision tree strictly compliant with the flowchart image.
        Garde-fou : si count < MIN_TE_SAMPLES, Te est ramené à 0 (non fiable).
        """
        te = metrics.get("Te", 0.0)
        te_count = metrics.get("Te_count", 0)
        he = metrics.get("He", 0.0)
        r_score = metrics.get("R", 0.0)
        freq = metrics.get("Freq", 0.0)
        yield_score = metrics.get("Yield", 0.0)

        # Garde-fou : Te non fiable si trop peu d'échantillons
        if te_count < self.MIN_TE_SAMPLES:
            te = 0.0

        # Derived metrics/proxies when not explicitly given yet in data
        feas_score = metrics.get("Feas", 0.0)
        domain_shift = metrics.get("DomainShift", 0.0)
        llm_necessity = metrics.get("LLM_Necessity", 0.0)
        path_trace = []
        method = "UNKNOWN"
        justification = ""

        def resolve(m, j):
            nonlocal method, justification
            method = m
            justification = j

        # ── NOEUD 1 : Templateabilité élevée ? ──
        path_trace.append("Templateabilité élevée?")
        if te >= self.THRESHOLDS["TE_HIGH"]:
            path_trace.append("Oui -> Variabilité lexicale faible?")
            if he >= self.THRESHOLDS["HE_HIGH"]:
                path_trace.append("Oui -> Risque contextuel faible?")
                if r_score < self.THRESHOLDS["RISK_HIGH"]:
                    path_trace.append("Oui -> [RÈGLES]")
                    resolve("RÈGLES", "Temp élevée, var lexicale faible, certitude contextuelle élevée.")
                    return {"method": method, "justification": justification, "trace": path_trace}
                else:
                    # Te élevée + He élevée + R élevé → Faisabilité NER
                    path_trace.append("Non (R élevé) -> Faisabilité NER élevée?")
            else:
                # Te élevée MAIS He faible → sauter directement à Faisabilité NER
                # (ne pas re-tester Te moyenne car Te est déjà haute)
                path_trace.append("Non (He faible) -> Faisabilité NER élevée?")
        else:
            # ── NOEUD 1b : Homogénéité lexicale élevée + Yield confirme ? ──
            # Si He très élevée, R faible ET Yield > 0 (les règles trouvent au moins
            # quelque chose), alors les règles sont appropriées.
            # Si Yield trop faible, les règles ne fonctionnent pas suffisamment → on continue.
            path_trace.append("Non -> Homogénéité élevée + Yield ≥ seuil?")
            if he >= self.THRESHOLDS["HE_HIGH"] and r_score < self.THRESHOLDS["RISK_HIGH"] and yield_score >= self.THRESHOLDS["YIELD_MIN_RULES"]:
                path_trace.append(f"Oui (He={he:.1f}%, R={r_score:.2f}, Yield={yield_score:.2f}) -> [RÈGLES]")
                resolve("RÈGLES",
                        f"He très élevée ({he:.1f}%), risque faible ({r_score:.2f}), Yield={yield_score:.2f} confirme l'efficacité des règles.")
                return {"method": method, "justification": justification, "trace": path_trace}
            else:
                # ── NOEUD 2 : Templateabilité moyenne ? ──
                path_trace.append("Non -> Templateabilité moyenne?")
                if te >= self.THRESHOLDS["TE_MED"]:
                    path_trace.append("Oui -> Fréquence suffisante?")
                    if freq >= self.THRESHOLDS["FREQ_MIN"]:
                        path_trace.append("Oui -> Rendement d'annotation suffisant?")
                        if yield_score >= self.THRESHOLDS["YIELD_HIGH"]:
                            path_trace.append("Oui -> [ML LÉGER]")
                            resolve("ML LÉGER", "Temp structurelle moyenne mais grand volume de données de qualité.")
                            return {"method": method, "justification": justification, "trace": path_trace}
                        else:
                            path_trace.append("Non -> Faisabilité NER élevée?")
                    else:
                        path_trace.append("Non -> Faisabilité NER élevée?")
                else:
                    path_trace.append("Non -> Faisabilité NER élevée?")

        # CHEMIN : Faisabilité NER élevée
        if path_trace[-1].endswith("Faisabilité NER élevée?"):
            if feas_score >= self.THRESHOLDS["FEAS_NER"]:
                path_trace.append("Oui -> Décalage de domaine faible?")
                if domain_shift < self.THRESHOLDS["DOMAIN_SHIFT_MAX"]:
                    path_trace.append("Oui -> [TRANSFORMER BIDIRECTIONNEL]")
                    resolve("TRANSFORMER BIDIRECTIONNEL", "Données faisables et domaine concordant pour Transformers.")
                    return {"method": method, "justification": justification, "trace": path_trace}
                else:
                    path_trace.append("Non -> Nécessité LLM élevée?")
            else:
                path_trace.append("Non -> Nécessité LLM élevée?")

        # CHEMIN : Nécessité LLM élevée
        if path_trace[-1].endswith("Nécessité LLM élevée?"):
            if llm_necessity >= self.THRESHOLDS["LLM_NEC_HIGH"]:
                path_trace.append("Oui -> [LLM]")
                resolve("LLM", "Forte complexité/nécessité d'utiliser un LLM lourd.")
                return {"method": method, "justification": justification, "trace": path_trace}
            else:
                path_trace.append("Non -> Fréquence suffisante?")
                if freq >= self.THRESHOLDS["FREQ_MIN"]:
                    path_trace.append("Oui -> [ML LÉGER PAR DÉFAUT]")
                    resolve("ML LÉGER PAR DÉFAUT", "Backoff : ML léger retenu par défaut (fréquences acceptables).")
                    return {"method": method, "justification": justification, "trace": path_trace}
                else:
                    path_trace.append("Non -> [RÈGLES PAR DÉFAUT]")
                    resolve("RÈGLES PAR DÉFAUT", "Backoff final : Fréquence trop faible, utilisation de règles par défaut.")
                    return {"method": method, "justification": justification, "trace": path_trace}

        # Sécurité
        return {"method": method, "justification": justification, "trace": path_trace}

    def build_full_config(self, metrics_data: Dict[str, Dict]):
        """Compile all decisions into the config dict."""
        config = {
            "version": "2.1",
            "global_thresholds": self.THRESHOLDS,
            "entities": {},
        }

        print("\n=== DECISION TREE EXECUTION ===")
        print(f"{'Entity':<25} | {'Method':<18} | {'Justification'}")
        print("-" * 100)

        for entity_raw, mets in metrics_data.items():
            # Clean entity name if needed
            entity = entity_raw.strip()
            decision = self.analyze_entity(entity, mets)

            # Print short reason
            reason_short = (
                (decision["justification"][:75] + "..")
                if len(decision["justification"]) > 75
                else decision["justification"]
            )
            print(f"{entity:<25} | {decision['method']:<18} | {reason_short}")

            config["entities"][entity] = {
                "metrics": mets,
                "method": decision["method"],
                "justification": decision["justification"],
                "trace": decision["trace"],
            }

        self.decisions = config
        return config

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.decisions, f, indent=4)
        print(f"\nConfiguration saved to {self.config_path}")

    def export_text_report(self, output_txt: Path):
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write("# DuraXELL Decision Tree Report\n")
            f.write("Generated by E_creation_arbre_decision.py\n\n")
            f.write("## Global Thresholds:\n")
            for k, v in self.THRESHOLDS.items():
                f.write(f"- {k}: {v}\n")
            f.write("\n")

            for entity, data in self.decisions["entities"].items():
                f.write(f"## {entity}\n")
                f.write(f"- **Method**: {data['method']}\n")
                f.write(f"- **Justification**: {data['justification']}\n")
                f.write(
                    f"- **Metrics**: {json.dumps(data['metrics'], default=str)}\n"
                )  # default=str to handle non serializable
                f.write(f"- **Trace**: {' -> '.join(data['trace'])}\n\n")
        print(f"Report saved to {output_txt}")


def load_metrics_from_csv(results_dir: Path):
    """Aggregate CSV results from previous steps into a single dict."""
    aggregated = {}  # {Entity: {Te: x, He: y...}}

    def _read_csv(filename, col_name, metric_key, multiplier=1.0):
        p = results_dir / filename
        if not p.exists():
            return
        try:
            with open(p, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Try different column headers for Entity name
                    ent = (
                        row.get("Entity") or row.get("Entity_Type") or row.get("Entité")
                    )
                    if not ent:
                        continue

                    try:
                        val = float(row.get(col_name, 0))
                        if ent not in aggregated:
                            aggregated[ent] = {}
                        aggregated[ent][metric_key] = val * multiplier
                    except ValueError:
                        pass
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # 1. Te (Templeability)
    # Often in JSON, but let's check CSVs too
    if (results_dir / "templeability_analysis.json").exists():
        try:
            with open(results_dir / "templeability_analysis.json") as f:
                data = json.load(f)
                for ent, vals in data.items():
                    if ent not in aggregated:
                        aggregated[ent] = {}
                    aggregated[ent]["Te"] = vals.get("templeability_score", 0)
                    aggregated[ent]["Te_count"] = vals.get("count", 0)
        except:
            pass

    # 2. He (Homogeneity)
    _read_csv("homogeneity_analysis.csv", "He_Score_Percent", "He")

    # 3. R (Risk)
    _read_csv("risk_context_analysis.csv", "R_Score", "R")

    # 4. Freq (Frequency)
    _read_csv("frequency_analysis.csv", "Frequency", "Freq")

    # 5. NER Feasibility metrics
    _read_csv("ner_feasibility_analysis.csv", "Feas_Score", "Feas")
    _read_csv("ner_feasibility_analysis.csv", "Domain_Shift", "DomainShift")
    _read_csv("ner_feasibility_analysis.csv", "LLM_Necessity", "LLM_Necessity")

    return aggregated


def main():
    SCRIPT_DIR = Path(__file__).parent
    # Standard DuraXELL directory structure
    RESULTS_DIR = SCRIPT_DIR / "Rules/Results"
    ROOT_DIR = SCRIPT_DIR.parent
    CONFIG_FILE = ROOT_DIR / "decision_config.json"
    REPORT_FILE = ROOT_DIR / "output_decision.txt"

    # 1. Load existing metrics
    print("Loading metrics from Results folder...")
    metrics_db = load_metrics_from_csv(RESULTS_DIR)

    # 2. Compute Yield on the fly (Hybrid approach)
    # We define paths to GS and Pred
    gs_dir = SCRIPT_DIR / "Breast/RCP/evaluation_set_breast_cancer_GS"
    pred_dir = (
        SCRIPT_DIR / "Breast/RCP/evaluation_set_breast_cancer_pred_rules"
    )

    # If using CHIR as well? For now stick to RCP as primary benchmark

    if gs_dir.exists() and pred_dir.exists():
        try:
            print("Computing Annotation Yield (Rules vs GS)...")
            yield_scorer = AnnotationYieldScorer(gs_dir, pred_dir)
            yield_scorer.compute_all()
            yield_scores = yield_scorer.get_scores()

            for ent, score_dict in yield_scores.items():
                f1 = score_dict.get("F1-Yield", 0.0) if isinstance(score_dict, dict) else float(score_dict)
                if ent in metrics_db:
                    metrics_db[ent]["Yield"] = f1
                else:
                    metrics_db[ent] = {"Yield": f1}  # If missing in other stats
            print("Annotation Yield computed.")
        except NameError:
            print(
                "AnnotationYieldScorer class not found (import failed). Skipping Yield."
            )
    else:
        print(
            f"Warning: GS/Pred folders not found for Yield calculation.\nScan path: {gs_dir}"
        )

    # 3. Build Tree
    builder = DecisionTreeBuilder(CONFIG_FILE)
    builder.validate_thresholds_kfold(metrics_db, k=3)
    builder.build_full_config(metrics_db)

    # 4. Save Outputs
    builder.save_config()
    builder.export_text_report(REPORT_FILE)
    if HAS_ECO2AI:
        try:
            tracker.stop()
        except Exception:
            pass


if __name__ == "__main__":
    main()
