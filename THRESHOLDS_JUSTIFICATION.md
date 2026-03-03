# Justification des Seuils de l'Arbre de Décision DuraXELL

Ce document explicite les choix statistiques et empiriques derrière les seuils utilisés dans `E_creation_arbre_decision.py` pour router les entités vers la méthode d'extraction optimale (Règles, ML, Transformer, LLM).

> **Garde-fou** : si le nombre d'occurrences d'une entité est < 10, le score Te est ramené à 0 (non fiable statistiquement).

## 1. Templateability (Te)
**Définition** : Mesure la stabilité structurelle d'une entité (à quel point elle s'écrit toujours de la même façon). Échelle 0–100.

*   **`TE_HIGH = 70.0`**
    *   *Justification* : Une entité avec Te ≥ 70 signifie que plus de 70 % de ses occurrences suivent un nombre très restreint de motifs (patterns). Seules les entités hautement prédictibles sont envoyées directement au moteur de règles.
*   **`TE_MED = 40.0`**
    *   *Justification* : Une entité avec 40 ≤ Te < 70 a une variabilité modérée. Si la fréquence et le rendement d'annotation sont suffisants, un ML léger peut être efficace. En dessous de 40, on passe aux vérifications de faisabilité NER.

## 2. Homogénéité (He)
**Définition** : Mesure la variabilité lexicale (le nombre de mots uniques utilisés pour décrire l'entité). Échelle 0–100.

*   **`HE_HIGH = 70.0`**
    *   *Justification* : Utilisé en conjonction avec `TE_HIGH`. Même si une entité a une structure stable (Te élevé), si le vocabulaire utilisé est trop varié (He < 70), les règles basées sur des dictionnaires stricts vont rater des occurrences. Un He ≥ 70 confirme que le vocabulaire est suffisamment restreint pour qu'un dictionnaire exhaustif soit maintenable.

## 3. Risque Contextuel (R)
**Définition** : Probabilité que l'entité soit entourée de négations, d'incertitudes ou de contradictions. Échelle 0–1.

*   **`RISK_HIGH = 0.50`**
    *   *Justification* : Si plus de 50 % des mentions d'une entité sont dans un contexte ambigu ou négatif, les méthodes simples (Règles, ML léger) risquent de générer des faux positifs. Au-delà de ce seuil, l'arbre privilégie des modèles à capacité contextuelle (Transformers, LLM).

## 4. Fréquence (Freq)
**Définition** : Rareté de l'entité dans le corpus. Échelle 0–1.

*   **`FREQ_MIN = 0.001`** (soit 1 occurrence pour 1000 tokens)
    *   *Justification* : Les modèles ML nécessitent un volume minimum de données d'entraînement. Si une entité est trop rare (Freq < 0.001), l'entraînement est impossible ou sujet au surapprentissage.

## 5. Rendement d'Annotation (Yield)
**Définition** : F1-score du système de règles par rapport au Gold Standard. Échelle 0–1.

*   **`YIELD_HIGH = 0.75`**
    *   *Justification* : Garde-fou avant d'assigner une entité au ML Léger. Si le rendement des règles est ≥ 0.75, un ML léger peut affiner. Sinon, on vérifie la faisabilité NER.

## 6. Faisabilité NER (Feas)
**Définition** : Score composite (Freq + He + Yield) reflétant la viabilité d'une approche NER Transformer. Échelle 0–1.

*   **`FEAS_NER = 0.6`**
    *   *Justification* : Un Feas ≥ 0.6 indique que les données sont suffisamment abondantes, homogènes et annotables pour entraîner un Transformer bidirectionnel efficacement.

## 7. Décalage de Domaine (DomainShift)
**Définition** : Mesure de l'écart entre le corpus d'entraînement et les documents cibles. Échelle 0–1.

*   **`DOMAIN_SHIFT_MAX = 0.5`**
    *   *Justification* : Un décalage ≥ 0.5 rend un Transformer pré-entraîné peu fiable. L'arbre escalade vers un LLM en zero/few-shot.

## 8. Nécessité LLM (LLM_Necessity)
**Définition** : Score composite reflétant la complexité résiduelle nécessitant un LLM. Échelle 0–1.

*   **`LLM_NEC_HIGH = 0.5`**
    *   *Justification* : Au-delà de 0.5, la complexité (faible Yield, risque élevé, faible faisabilité) justifie le coût énergétique d'un LLM.
