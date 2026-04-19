"""
Generate HTML report for Risk Context analysis.
"""

import json
from pathlib import Path


def generate_html_report(json_file: str, csv_file: str, output_file: str):
    """
    Generate an HTML report from risk context analysis results.

    Args:
        json_file: Path to the JSON report file
        csv_file: Path to the CSV report file
        output_file: Path to save the HTML report
    """

    # Load data
    with open(json_file, encoding="utf-8") as f:
        report_data = json.load(f)

    # We can use the JSON data directly as it contains the same info as CSV usually
    # But ensuring we implement sorting
    data_list = report_data

    # Sort by Risk Score descending (Highest Risk at top)
    data_list.sort(key=lambda x: x.get("Risk_Score", 0), reverse=True)

    # Calculate stats
    total_entities = len(data_list)
    avg_score = (
        sum(item.get("Risk_Score", 0) for item in data_list) / total_entities
        if total_entities > 0
        else 0
    )
    high_risk_count = sum(1 for item in data_list if item.get("Risk_Score", 0) >= 0.7)

    # Create HTML
    html_content = (
        """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport d'Analyse du Risque Contextuel</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }

            .container {
                max_width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }

            header {
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
            }

            h1 {
                color: #2c3e50;
                font-size: 2.5em;
                margin-bottom: 10px;
            }

            p.desc {
                color: #7f8c8d;
                font-size: 1.1em;
                max_width: 800px;
                margin: 0 auto;
            }

            .summary-section {
                display: flex;
                justify-content: space-around;
                margin-bottom: 40px;
                gap: 20px;
                flex-wrap: wrap;
            }

            .summary-card {
                flex: 1;
                min-width: 200px;
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid #e2e8f0;
            }

            .summary-card .label {
                font-weight: 600;
                color: #718096;
                margin-bottom: 10px;
                text-transform: uppercase;
                font-size: 0.85em;
                letter-spacing: 0.05em;
            }

            .summary-card .value {
                font-size: 2em;
                font-weight: bold;
            }

            .entity-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }

            .entity-card {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                transition: all 0.3s ease;
            }

            .entity-card:hover {
                box-shadow: 0 5px 15px rgba(255, 107, 107, 0.2);
                border-color: #FF6B6B;
            }

            /* High Risk = Red */
            .entity-card.high-risk {
                border-left: 5px solid #ef4444;
            }

            /* Medium Risk = Yellow */
            .entity-card.medium-risk {
                border-left: 5px solid #f59e0b;
            }

            /* Low Risk = Green */
            .entity-card.low-risk {
                border-left: 5px solid #22c55e;
            }

            .entity-name {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 15px;
                color: #e53e3e;
            }

            .score-bar {
                display: flex;
                align-items: center;
                margin: 15px 0;
            }

            .score-bar-label {
                width: 150px;
                font-weight: 500;
            }

            .score-bar-fill {
                flex: 1;
                height: 25px;
                background: #e5e7eb;
                border-radius: 4px;
                overflow: hidden;
                margin: 0 10px;
            }

            .score-bar-value {
                height: 100%;
                /* Gradient Red to Orange */
                background: linear-gradient(90deg, #FF6B6B 0%, #FF8E53 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 0.9em;
            }

            .score-text {
                width: 80px;
                text-align: right;
                font-weight: bold;
            }

            .metric {
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
                font-size: 0.95em;
            }

            .metric-label {
                font-weight: 500;
            }

            .metric-value {
                color: #e53e3e;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Rapport de Risque Contextuel</h1>
                <p class="desc">
                    Analyse de la probabilité d ambiguïté nécessitant une analyse contextuelle approfondie.
                    <br>
                    <strong>Risque Faible:</strong> Entités non ambiguës ou auto-décrites.
                    <strong>Risque Élevé:</strong> Termes polysémiques nécessitant un contexte externe.
                </p>
            </header>

            <div style="background: #f1f5f9; padding: 20px; border-radius: 8px; margin-bottom: 40px; border-left: 5px solid #64748b;">
                <h3 style="color: #475569; margin-bottom: 10px;">Méthodologie & Implémentation</h3>
                <ul style="list-style-type: none; padding-left: 0; color: #334155; line-height: 1.6;">
                    <li style="margin-bottom: 10px;">
                        <strong>1. Détection d'Ambiguïté (Calcul des "Mentions à Haut Risque"):</strong>
                        Une "Mention à Haut Risque" est une valeur extraite qui est :
                        <ul style="margin-top:5px; margin-bottom:5px;">
                            <li>Soit un terme générique polysémique (ex: <em>"Positif", "Score 3", "++"</em>) pouvant s'appliquer à plusieurs entités.</li>
                            <li>Soit un chiffre nu ou pourcentage (ex: <em>"10%", "3"</em>) sans le nom de l'entité à l'intérieur de la chaîne de caractères.</li>
                        </ul>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <strong>2. Vérification d'Auto-Description (Atténuation):</strong>
                        Vérifie si le texte extrait contient le nom de l'entité (ex: <em>"Ki67 10%"</em> contient "Ki67").
                        <span style="color: #22c55e; font-weight: bold;">Une valeur explicite annule le risque -> Risque Faible.</span>
                    </li>
                    <li style="margin-bottom: 10px;">
                        <strong>3. Reconnaissance de Motifs Structurés:</strong>
                        Identifie les formats complexes (ex: <em>"pT2N0M1"</em>) qui sont intrinsèquement spécifiques.
                    </li>
                    <li>
                        <strong>Formule de Calcul:</strong>
                        <code>Score de Risque = (Mentions à Haut Risque) / (Total des Mentions)</code>.
                    </li>
                </ul>
                <div style="background: #fff1f2; border-left: 5px solid #e11d48; padding: 15px; margin-top: 15px; color: #881337; font-size: 0.95em;">
                    <strong>Pourquoi mon score est-il de 0 ?</strong>
                    <p style="margin: 5px 0 0 0;">
                        Un score de <strong>0.0</strong> indique que toutes les valeurs extraites pour cette entité sont "Auto-Décrites" ou non-ambiguës.
                        Cela signifie que vos annotations incluent systématiquement le nom du biomarqueur (ex: vous avez extrait <em>"HER2 positif"</em> et non juste <em>"positif"</em>).
                        C'est le signe d'une excellente qualité d'extraction.
                    </p>
                </div>
            </div>

            <div class="summary-section">
                <div class="summary-card">
                    <div class="label">Total Entités Analysées</div>
                    <div class="value">"""
        + str(total_entities)
        + """</div>
                </div>
                <div class="summary-card">
                    <div class="label">Score Moyen</div>
                    <div class="value">"""
        + f"{avg_score:.2f}"
        + """</div>
                </div>
                <div class="summary-card">
                    <div class="label">Entités à Risque Élevé</div>
                    <div class="value">"""
        + str(high_risk_count)
        + """</div>
                </div>
            </div>

            <div class="entity-grid">
    """
    )

    for row in data_list:
        score = row["Risk_Score"]
        risk_class = "low-risk"
        if score >= 0.7:
            risk_class = "high-risk"
        elif score >= 0.3:
            risk_class = "medium-risk"

        width_pct = max(5, int(score * 100))

        metrics_html = f"""
            <div class="metric">
                <span class="metric-label">Classe de Risque:</span>
                <span class="metric-value">{row["Risk_Class"]}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Total Mentions:</span>
                <span class="metric-value">{row["Total_Mentions"]}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Taux de Polysémie:</span>
                <span class="metric-value">{row["Polysemy_Rate"]}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Ambiguïté Numérique:</span>
                <span class="metric-value">{row["Numeric_Ambiguity_Rate"]}</span>
            </div>
             <div class="metric">
                <span class="metric-label">Taux d'Auto-Description:</span>
                <span class="metric-value" style="color:#22c55e">{row["Self_Described_Rate"]}</span>
            </div>
        """

        card_html = f"""
        <div class="entity-card {risk_class}">
            <div class="entity-name">{row["Entity"]}</div>

            <div class="score-bar">
                <div class="score-bar-label">Score Risque</div>
                <div class="score-bar-fill">
                    <div class="score-bar-value" style="width: {width_pct}%">{score:.2f}</div>
                </div>
                <div class="score-text">{score:.2f}</div>
            </div>

            {metrics_html}
        </div>
        """
        html_content += card_html

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML Report generated: {output_file}")


if __name__ == "__main__":
    # Example usage based on workspace structure
    try:
        # Correct directory from project root is Results
        project_root = Path(__file__).parent.parent
        base_dir = project_root / "Results"

        json_path = base_dir / "risk_context_full.json"
        csv_path = base_dir / "risk_context_summary.csv"
        html_path = base_dir / "risk_context_analysis_report.html"

        if json_path.exists() and csv_path.exists():
            generate_html_report(str(json_path), str(csv_path), str(html_path))
        else:
            print("Usage: Call this script after running risk_context.py")
            print(f"Looking for data in: {base_dir}")
            print(f"JSON exists: {json_path.exists()}")
    except Exception as e:
        print(f"Error: {e}")

try:
    tracker.stop()
except Exception as e:
    print(
        f"\nWarning: Generalized error in Eco2AI tracking (likely 'N/A' vs float dtype issue): {e}"
    )
    print(
        "Carbon emission tracking data could not be saved, but analysis results are preserved."
    )
