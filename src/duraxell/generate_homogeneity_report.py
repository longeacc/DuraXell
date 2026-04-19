"""
Generate HTML report for Homogeneity analysis.
"""

import csv
from pathlib import Path


def generate_html_report(csv_file: str, output_file: str):
    """
    Generate an HTML report from homogeneity analysis results (CSV).

    Args:
        csv_file: Path to the CSV report file
        output_file: Path to save the HTML report
    """

    # Load data from CSV
    data = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields back to float/int where possible
                try:
                    row["Homogeneity_Score"] = float(row.get("Homogeneity_Score", 0))
                    row["Homogeneity_Raw_He"] = float(row.get("Homogeneity_Raw_He", 0))
                    row["Structural_Templatability"] = float(
                        row.get("Structural_Templatability", 0)
                    )
                    row["Unique_Words_Ue"] = float(row.get("Unique_Words_Ue", 0))
                    row["Total_Words_Te"] = float(row.get("Total_Words_Te", 0))
                except ValueError:
                    continue
                data.append(row)
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_file}")
        return

    # Sort data by score descending
    data.sort(key=lambda x: x["Homogeneity_Score"], reverse=True)

    # HTML Template
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Analyse d'Homogénéité Linguistique</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f1f5f9; padding: 40px; color: #333; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #334155; text-align: center; margin-bottom: 20px; }
            
            .method-box { background: #e0f2fe; border-left: 5px solid #0ea5e9; padding: 20px; margin-bottom: 30px; }
            .formula { font-family: monospace; font-weight: bold; font-size: 1.1em; color: #0369a1; background: rgba(255,255,255,0.5); padding: 5px; border-radius: 4px; display: inline-block; margin: 5px 0; }
            
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { background: #475569; color: white; padding: 12px; text-align: left; }
            td { padding: 12px; border-bottom: 1px solid #e2e8f0; }
            tr:hover { background: #f8fafc; }
            
            .badge { padding: 4px 10px; border-radius: 15px; font-weight: bold; color: white; font-size: 0.9em; }
            .high { background: #22c55e; }
            .medium { background: #f59e0b; }
            .low { background: #b91c1c; }
            
            .footer { margin-top: 40px; text-align: center; font-size: 0.9em; color: #888; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Homogénéité Linguistique (He) vs Templeabilité (Te)</h1>
            
            <div class="method-box">
                <h3>Méthodologie & Définitions</h3>
                <p><strong>Homogénéité Linguistique (He):</strong> Mesure la redondance lexicale, c'est-à-dire la fréquence à laquelle le même vocabulaire est réutilisé pour une entité donnée.</p>
                <p>Une homogénéité élevée indique un vocabulaire très contrôlé et répétitif (peu de variation dans les mots utilisés).</p>
                
                <p><strong>Formules:</strong></p>
                <div class="formula">He = (TotalMots - MotsUniques) / TotalMots</div>
                <br>
                <div class="formula">Score = Sigmoïde(He)</div>
                <p style="font-size: 0.9em; margin-top: 10px;"><em>Le score est normalisé par une fonction sigmoïde pour accentuer les différences proches de 0.5.</em></p>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Type d'Entité</th>
                        <th>Homogénéité (Score)</th>
                        <th>He Brut (Redondance)</th>
                        <th>Templeabilité (Structure)</th>
                        <th>Stats Mots (Uniques/Total)</th>
                    </tr>
                </thead>
                <tbody>
    """

    for row in data:
        s = row["Homogeneity_Score"]
        cls = "high" if s > 0.8 else "medium" if s > 0.5 else "low"

        html_content += f"""
                <tr>
                    <td><strong>{row["Entity_Type"]}</strong></td>
                    <td><span class="badge {cls}">{s:.4f}</span></td>
                    <td>{row["Homogeneity_Raw_He"]:.4f}</td>
                    <td>{row["Structural_Templatability"]:.4f}</td>
                    <td>{int(row["Unique_Words_Ue"])} / {int(row["Total_Words_Te"])}</td>
                </tr>
        """

    html_content += """
                </tbody>
            </table>
            
            <div style="margin-top: 30px; font-size: 0.9em; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 20px;">
                <p><strong>Note d'Interprétation:</strong></p>
                <ul style="margin-top: 5px;">
                    <li><strong>Haute Homogénéité:</strong> Vocabulaire très restreint et répétitif.</li>
                    <li><strong>Haute Templeabilité:</strong> Respect strict de formats structurels (types de caractères, ponctuation).</li>
                    <li>Ces deux métriques corrèlent souvent mais mesurent deux aspects distincts de la qualité des données (Lexical vs Structurel).</li>
                </ul>
            </div>
            
            <div class="footer">Rapport généré automatiquement - ESMO 2025</div>
        </div>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Rapport HTML généré: {output_file}")


if __name__ == "__main__":
    # Determine the project root (duraxell_Clement)
    # Assuming this script is in src/duraxell/generate_homogeneity_report.py
    current_dir = Path(__file__).parent

    # The output CSV is likely in src/duraxell/Results or src/duraxell/Rules/src/Results (based on workspace info)
    # Let's check a few likely locations
    possible_csv_paths = [
        current_dir / "Results/homogeneity_analysis.csv",
        current_dir / "Rules/src/Results/homogeneity_analysis.csv",
        current_dir.parent / "Results/homogeneity_analysis.csv",
    ]

    csv_path = None
    for p in possible_csv_paths:
        if p.exists():
            csv_path = p
            break

    if csv_path:
        html_path = csv_path.with_suffix(".html")
        generate_html_report(str(csv_path), str(html_path))
    else:
        # If no CSV found, we can't generate.
        print(
            f"Fichier CSV introuvable dans les chemins testés: {[str(p) for p in possible_csv_paths]}"
        )

try:
    tracker.stop()
except Exception as e:
    print(
        f"\nWarning: Generalized error in Eco2AI tracking (likely 'N/A' vs float dtype issue): {e}"
    )
    print(
        "Carbon emission tracking data could not be saved, but analysis results are preserved."
    )
