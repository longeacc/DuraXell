print("Start import")
try:
    from ESMO2025.E_frequency import FrequencyScorer
    print("Import successful")
    scorer = FrequencyScorer([])
    print("Instantiation successful")
except Exception as e:
    print(f"Error: {e}")
print("End script")
