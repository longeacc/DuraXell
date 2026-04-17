def compute_routing(metrics, thresholds):
    Te, He, R = metrics.get("Te", 0), metrics.get("He", 0), metrics.get("R", 0)
    Freq, Yield = metrics.get("Freq", 0), metrics.get("Yield", 0)
    DS, Feas = metrics.get("DomainShift", 0), metrics.get("Feas", 0)
    LLM_N = metrics.get("LLM_Necessity", 0)
    
    # Règle 1 : S'il y a un rendement fort (Yield), la regex marche ! On route vers RULES
    if Yield >= thresholds.get("Yield", 0.5):
        return "RULES", f"Yield={Yield}>={thresholds.get('Yield', 0.5)}", Yield
        
    # Règle 2 : Si l'entropie et la régularité sont bonnes, on route vers RULES
    if Te >= thresholds.get("Te", 0.5) and He >= thresholds.get("He", 0.5) and R <= thresholds.get("R", 0.5):
        return "RULES", f"Te={Te}>={thresholds.get('Te', 0.5)}, He={He}>={thresholds.get('He', 0.5)}", Te * 0.8 + He * 0.2
        
    # Règle 3 : Transformer si Faisabilité et Décalage gérables
    if DS >= thresholds.get("DomainShift", 0.5) and Feas >= thresholds.get("Feas", 0.5):
        return "TRANSFORMER", f"Feas={Feas}>={thresholds.get('Feas', 0.5)}", Feas
        
    return "LLM", f"LLM_Necessity={LLM_N}", LLM_N
