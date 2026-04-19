import argparse
import csv
import glob
import logging
import os
import sys
import subprocess
import time



# All entity types known to the decision tree
ALL_ENTITIES = [
    "Estrogen_receptor",
    "Progesterone_receptor",
    "HER2_status",
    "HER2_IHC",
    "Ki67",
    "HER2_FISH",
    "Genetic_mutation",
]


def cmd_extract(args):
    """Run cascade extract on a single document"""
    from duraxell.cascade_orchestrator import CascadeOrchestrator

    orchestrator = CascadeOrchestrator()
    print(f"Extraction for entity '{args.entity}':")
    res = orchestrator.extract(args.doc, args.entity)
    print(
        f"Result: {res.value} | Method: {res.method_used} | Confidence: {res.confidence} | Energy: {res.energy_kwh:.6f} kWh"
    )


def cmd_extract_all(args):
    """Extract ALL known entities from a single document."""
    from duraxell.cascade_orchestrator import CascadeOrchestrator

    orchestrator = CascadeOrchestrator()
    entities = args.entities.split(",") if args.entities else ALL_ENTITIES
    print(f"Extraction de {len(entities)} entitÃ©s depuis le document...")
    print("-" * 80)
    total_energy = 0.0
    for ent in entities:
        ent = ent.strip()
        res = orchestrator.extract(args.doc, ent)
        status = res.value if res.value else "NON TROUVÃ‰"
        print(
            f"  {ent:<25s} => {status:<20s} | {res.method_used:<12s} | conf={res.confidence:.2f} | E={res.energy_kwh:.6f} kWh"
        )
        total_energy += res.energy_kwh
    print("-" * 80)
    print(f"  Ã‰nergie totale : {total_energy:.6f} kWh")


def cmd_batch(args):
    """Extract entities from all .txt files in a directory.
    Produces a CSV file in Results/ with columns:
      fichier, entite, valeur, methode, confiance, energie_kwh, methode_recommandee
    """
    # Suppress noisy NER/eco2ai warnings during batch
    logging.basicConfig(level=logging.WARNING)

    from duraxell.cascade_orchestrator import CascadeOrchestrator
    import json

    orchestrator = CascadeOrchestrator()
    input_dir = args.input_dir
    entities = (
        [e.strip() for e in args.entities.split(",")] if args.entities else ALL_ENTITIES
    )
    files = sorted(glob.glob(os.path.join(input_dir, "*.txt")))
    if not files:
        print(f"Aucun fichier .txt trouvÃ© dans {input_dir}")
        return

    # Load decision_config to get the recommended method per entity
    decision_cfg = {}
    cfg_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "decision_config.json"
    )
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            decision_cfg = raw.get("entities", raw)

    # Prepare output
    os.makedirs("Results", exist_ok=True)
    out_path = os.path.join("Results", "batch_extraction_results.csv")

    rows = []
    total = len(files) * len(entities)
    done = 0
    t0 = time.time()

    print(
        f"Batch : {len(files)} fichiers Ã— {len(entities)} entitÃ©s = {total} extractions"
    )
    print(f"Sortie CSV : {out_path}")
    print("-" * 70)

    for fpath in files:
        text = open(fpath, "r", encoding="utf-8").read()
        fname = os.path.basename(fpath)
        for ent in entities:
            res = orchestrator.extract(text, ent)
            ent_cfg = decision_cfg.get(ent, {})
            metrics = ent_cfg.get("metrics", {})
            rows.append(
                {
                    "fichier": fname,
                    "entite": ent,
                    "valeur": res.value if res.value else "",
                    "methode_utilisee": res.method_used,
                    "confiance": round(res.confidence, 4),
                    "energie_kwh": round(res.energy_kwh, 8),
                    "Te": metrics.get("Te", ""),
                    "He": metrics.get("He", ""),
                    "Freq": round(metrics["Freq"], 6) if "Freq" in metrics else "",
                    "Feas": metrics.get("Feas", ""),
                    "DomainShift": metrics.get("DomainShift", ""),
                    "LLM_Necessity": metrics.get("LLM_Necessity", ""),
                    "methode_recommandee": ent_cfg.get("method", ""),
                    "justification": ent_cfg.get("justification", ""),
                }
            )
            done += 1
            if done % 50 == 0 or done == total:
                elapsed = time.time() - t0
                print(
                    f"  [{done}/{total}] {elapsed:.1f}s - dernier: {fname} / {ent} => {res.value or '-'}"
                )

    # Write CSV
    fieldnames = [
        "fichier",
        "entite",
        "valeur",
        "methode_utilisee",
        "confiance",
        "energie_kwh",
        "Te",
        "He",
        "Freq",
        "Feas",
        "DomainShift",
        "LLM_Necessity",
        "methode_recommandee",
        "justification",
    ]
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")
        writer.writeheader()
        writer.writerows(rows)

    # Summary stats
    found = sum(1 for r in rows if r["valeur"])
    elapsed = time.time() - t0
    print("-" * 70)
    print(
        f"TerminÃ© en {elapsed:.1f}s | {found}/{total} extractions trouvÃ©es ({100 * found / total:.0f}%)"
    )
    print(f"CSV Ã©crit : {out_path} ({len(rows)} lignes)")


def cmd_metrics(args):
    """Compute ESMO2025 metrics"""
    print("Metrics running via specific scripts in src/duraxell/ ...")
    subprocess.run([sys.executable, "src/duraxell/E_templatability.py"])
    subprocess.run([sys.executable, "src/duraxell/E_homogeneity.py"])


def cmd_tree(args):
    """Generate and visualize the decision tree"""
    print("Generating decision tree...")
    subprocess.run([sys.executable, "src/duraxell/E_creation_arbre_decision.py"])
    print("Visualizing tree...")
    subprocess.run([sys.executable, "src/duraxell/visualize_decision_tree.py"])


def cmd_rest(args):
    """Launch REST demo or server"""
    print("Running REST Demo...")
    subprocess.run([sys.executable, "src/duraxell/REST_interface/demo_rest.py"])


def cmd_evaluate(args):
    """Run the full evaluation pipeline"""
    print("Running full report evaluation...")
    subprocess.run([sys.executable, "run_full_pipeline_report.py"])


def cmd_info(args):
    """Fetch info about the environment or model"""
    print("DuraXELL version: 2.0")
    print("Available components: Rules, NER, Transformers, LLM")


def main():
    parser = argparse.ArgumentParser(
        description="DuraXELL CLI - Central Hub for all commands"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: extract (single entity)
    parser_extract = subparsers.add_parser(
        "extract", help="Extract a single entity from a document text"
    )
    parser_extract.add_argument("--doc", type=str, required=True, help="Text document")
    parser_extract.add_argument(
        "--entity",
        type=str,
        required=True,
        help="Entity to extract (e.g. Estrogen_receptor)",
    )
    parser_extract.set_defaults(func=cmd_extract)

    # Command: extract-all (all entities at once)
    parser_extract_all = subparsers.add_parser(
        "extract-all", help="Extract ALL known entities from a document"
    )
    parser_extract_all.add_argument(
        "--doc", type=str, required=True, help="Text document"
    )
    parser_extract_all.add_argument(
        "--entities",
        type=str,
        default=None,
        help="Comma-separated entity list (default: all 7)",
    )
    parser_extract_all.set_defaults(func=cmd_extract_all)

    # Command: batch (directory of files Ã— entities)
    parser_batch = subparsers.add_parser(
        "batch", help="Extract entities from all .txt files in a directory"
    )
    parser_batch.add_argument(
        "--input_dir", type=str, required=True, help="Directory containing .txt files"
    )
    parser_batch.add_argument(
        "--entities",
        type=str,
        default=None,
        help="Comma-separated entity list (default: all 7)",
    )
    parser_batch.set_defaults(func=cmd_batch)

    # Command: metrics
    parser_metrics = subparsers.add_parser(
        "metrics", help="Run ESMO2025 metric pipelines"
    )
    parser_metrics.set_defaults(func=cmd_metrics)

    # Command: tree
    parser_tree = subparsers.add_parser(
        "tree", help="Generate decision tree and visual representation"
    )
    parser_tree.set_defaults(func=cmd_tree)

    # Command: rest
    parser_rest = subparsers.add_parser("rest", help="Start REST API tests and tools")
    parser_rest.set_defaults(func=cmd_rest)

    # Command: evaluate
    parser_evaluate = subparsers.add_parser(
        "evaluate", help="Compute metrics and generate reports"
    )
    parser_evaluate.set_defaults(func=cmd_evaluate)

    # Command: serve
    parser_serve = subparsers.add_parser(
        "serve", help="Serve DuraXELL model locally via HTTP (mock)"
    )
    parser_serve.set_defaults(
        func=lambda args: print("Serve mode is a work in progress.")
    )

    # Command: info
    parser_info = subparsers.add_parser(
        "info", help="Get basic configuration information"
    )
    parser_info.set_defaults(func=cmd_info)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
