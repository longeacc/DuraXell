import re

with open('ESMO2025/cascade_orchestrator.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'    def extract\(self, document: str, entity_type: str\) -> ExtractionResult:.*?# Niveau 4 : LLM \(Dernier recours\)\n\s+if \(not result\) or \(result\.confidence < self\.CONFIDENCE_THRESHOLDS\["LOW"\]\):'

replacement = """    def extract(self, document: str, entity_type: str) -> ExtractionResult:
        \"\"\"
        Point d'entrée principal. Exécute la logique de cascade.
        \"\"\"
        start_time = time.time()

        # 1. Déterminer la méthode recommandée
        recommended_method = self.decision_config.get(entity_type, {}).get(
            "method", "FEUILLE RÈGLES PAR DÉFAUT"
        )

        result = None

        # Mapping des méthodes de l'arbre vers les connecteurs techniques
        use_rules = recommended_method in [
            "FEUILLE NER À BASE DE RÈGLES", 
            "FEUILLE RÈGLES PAR DÉFAUT", 
            "REGLES", 
            "Rules"
        ]
        use_ml_transformer = recommended_method in [
            "FEUILLE ML LÉGER NER", 
            "FEUILLE ML LÉGER PAR DÉFAUT", 
            "FEUILLE NER TRANSFORMER BIDIRECTIONNEL", 
            "ML_NER", 
            "Transformer", 
            "CRF"
        ]
        use_llm = recommended_method in ["FEUILLE NER LLM", "LLM"]

        # Niveau 1 : REGLES
        if use_rules:
            result = self._try_rules(document, entity_type)
            if self._is_confident(result):
                result.execution_time_ms = (time.time() - start_time) * 1000
                return result
            # Sinon, cascade vers ML...

        # Niveau 2/3 : ML / Transformer
        # (Simplification : on groupe ML et Transformer ici sous "NER")
        if use_ml_transformer or not self._is_confident(result):
            ml_result = self._try_transformer(document, entity_type)

            # Si on vient d'un fallback règles, on garde le meilleur des deux ?
            # Pour l'instant, on prend le résultat ML s'il a une confiance correcte
            if self._is_confident(ml_result):
                ml_result.execution_time_ms = (time.time() - start_time) * 1000
                return ml_result
            result = ml_result

        # Niveau 4 : LLM (Dernier recours)
        if use_llm or (not result) or (result.confidence < self.CONFIDENCE_THRESHOLDS["LOW"]):"""

new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)

with open('ESMO2025/cascade_orchestrator.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Mapped CascadeOrchestrator successfully." if text != new_text else "Failed to map.")
