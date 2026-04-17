import os

file_path = "dashboard/pages/1_📊_Dashboard_Metriques.py"

with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

replacements = {
    "Mtriques": "Métriques",
    "dposez": "déposez",
    "chargs": "chargés",
    "Entits": "Entités",
    "donne": "donnée",
    "dtecte": "détectée",
    "Slectionner": "Sélectionner",
    "Dcision": "Décision",
    "Explicabilit": "Explicabilité",
    "Frugalit": "Frugalité",
    "Mathmatique": "Mathématique",
    "bas": "basé",
    "entit": "entité",
    "latrale": "latérale",
    "page_icon=\"??\"": 'page_icon="📊"',
    "?? Charger un corpus BRAT": "📂 Charger un corpus BRAT",
    "f\"? {len(documents)} documents": "f\"✅ {len(documents)} documents",
    "??? SEUILS DE ROUTAGE": "🎚️ SEUILS DE ROUTAGE",
    "?? STATISTIQUES CORPUS": "📊 STATISTIQUES CORPUS",
    "?? Dashboard des": "📊 Dashboard des",
    "?? Veuillez charger": "👈 Veuillez charger"
}

for bad, good in replacements.items():
    content = content.replace(bad, good)

# also check for ï¿½ if it was badly decoded
replacements_iso = {
    "Mï¿½triques": "Métriques",
    "dï¿½posez": "déposez",
    "chargï¿½s": "chargés",
    "Entitï¿½s": "Entités",
    "donnï¿½e": "donnée",
    "dï¿½tectï¿½e": "détectée",
    "Sï¿½lectionner": "Sélectionner",
    "Dï¿½cision": "Décision",
    "Explicabilitï¿½": "Explicabilité",
    "Frugalitï¿½": "Frugalité",
    "Mathï¿½matique": "Mathématique",
    "basï¿½": "basé",
    "entitï¿½": "entité",
    "latï¿½rale": "latérale"
}
for bad, good in replacements_iso.items():
    content = content.replace(bad, good)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Characters fixed and strictly saved as UTF-8.")
