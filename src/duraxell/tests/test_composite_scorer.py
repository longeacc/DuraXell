from duraxell.E_composite_scorer import CompositeScorer


def test_composite_scorer_logic():
    scorer = CompositeScorer()

    # Test 1: Rules (Perfect Expl, High Perf, Low Energy)
    # F1=0.9, Expl=1.0, Energy=0.0 -> Frugality=1.0
    # Composite = 0.4*0.9 + 0.3*1.0 + 0.3*1.0 = 0.36 + 0.3 + 0.3 = 0.96
    res_rules = scorer.compute(f1=0.9, method="Rules", energy_kwh=0.0)
    assert abs(res_rules - 0.96) < 0.001

    # Test 2: LLM (Low Expl, High Perf, High Energy)
    # F1=0.95, Expl=0.1, Energy=MAX -> Frugality=0.0
    # Composite = 0.4*0.95 + 0.3*0.1 + 0.3*0.0 = 0.38 + 0.03 = 0.41
    res_llm = scorer.compute(f1=0.95, method="LLM", energy_kwh=scorer.MAX_ENERGY_KWH)
    assert abs(res_llm - 0.41) < 0.001

    # Test 3: Transformer (Med Expl, High Perf, Med Energy)
    # F1=0.92, Expl=0.3, Energy=HALF_MAX -> Frugality=0.5
    # Composite = 0.4*0.92 + 0.3*0.3 + 0.3*0.5 = 0.368 + 0.09 + 0.15 = 0.608
    res_bert = scorer.compute(
        f1=0.92, method="Transformer", energy_kwh=scorer.MAX_ENERGY_KWH / 2
    )
    assert abs(res_bert - 0.608) < 0.001


def test_pareto_analysis():
    # Only need to mock pandas dataframe if not available, but test env should have pandas
    import pandas as pd

    scorer = CompositeScorer()

    # Scenario: Rules dominates LLM ?
    # Rules: F1=0.8, Expl=1.0, Energy=Low
    # LLM:   F1=0.81, Expl=0.1, Energy=High
    # LLM is NOT dominated strictly because F1 is better (0.81 > 0.8).
    # But Pareto front should include both usually unless one is worse everywhere.

    # Let's create a clear domination case
    # A: F1=0.9, Expl=1.0, Energy=Low
    # B: F1=0.8, Expl=0.5, Energy=High (Dominated by A)

    data = [
        {"Method": "A", "Entity": "E", "F1": 0.9, "Energy_kWh": 0.001},
        {
            "Method": "B",
            "Entity": "E",
            "F1": 0.8,
            "Energy_kWh": 0.01,
        },  # Worse F1, Worse Energy (High=Bad), Worse Expl (default 0.1)
    ]
    df = pd.DataFrame(data)

    # Adjust mock explains
    scorer.EXPLAINABILITY_SCORES = {"A": 1.0, "B": 0.5}

    res = scorer.pareto_analysis(df)

    # A should be Pareto (True)
    assert res.loc[0, "Is_Pareto"] == True
    # B should be Dominated (False)
    # F1(B) < F1(A) AND Expl(B) < Expl(A) AND Energy(B) > Energy(A)
    assert res.loc[1, "Is_Pareto"] == False
