# -*- coding: utf-8 -*-
import re

file_path = "dashboard/pages/1_📊_Dashboard_Metriques.py"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

# Emojis and missing accents fallback
text = text.replace('M\ufffdtriques', 'Métriques')
text = text.replace('d\ufffdposez', 'déposez')
text = text.replace('charg\ufffds', 'chargés')
text = text.replace('Entit\ufffds', 'Entités')
text = text.replace('donn\ufffde', 'donnée')
text = text.replace('d\ufffdtect\ufffde', 'détectée')
text = text.replace('S\ufffdlectionner', 'Sélectionner')
text = text.replace('D\ufffdcision', 'Décision')
text = text.replace('Explicabilit\ufffd', 'Explicabilité')
text = text.replace('Frugalit\ufffd', 'Frugalité')
text = text.replace('Math\ufffdmatique', 'Mathématique')
text = text.replace('bas\ufffd', 'basé')
text = text.replace('entit\ufffd', 'entité')
text = text.replace('lat\ufffdrale', 'latérale')
text = text.replace('page_icon="??"', 'page_icon="📊"')
text = text.replace('st.subheader("?? Charger un corpus BRAT")', 'st.subheader("📂 Charger un corpus BRAT")')
text = text.replace('st.success(f"?', 'st.success(f"✅')
text = text.replace('st.subheader("??? SEUILS DE ROUTAGE")', 'st.subheader("🎚️ SEUILS DE ROUTAGE")')
text = text.replace('st.subheader("?? STATISTIQUES CORPUS")', 'st.subheader("📊 STATISTIQUES CORPUS")')
text = text.replace('st.title("?? Dashboard des Métriques")', 'st.title("📊 Dashboard des Métriques")')
text = text.replace('st.info("?? Veuillez charger', 'st.info("👈 Veuillez charger')

# Remove duplicate é manually caused by my previous script
text = re.sub(r'é+', 'é', text) 
text = text.replace('bas\ufffd', 'basé')
text = text.replace('entité\ufffd', 'entité')
text = text.replace('Explicabilité\ufffd', 'Explicabilité')
text = text.replace('Frugalité\ufffd', 'Frugalité')
text = text.replace('donnée\ufffd', 'donnée')
text = text.replace('Mathématique\ufffd', 'Mathématique')
text = text.replace('détectée\ufffd', 'détectée')
text = text.replace('Entités\ufffd', 'Entités')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Accents and Emojis Fully Cleaned up.")
