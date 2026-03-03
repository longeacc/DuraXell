import re
from pathlib import Path

files = [
    "ESMO2025/Rules/src/Breast/lunch.py",
    "ESMO2025/generate_templeability_report.py",
    "ESMO2025/generate_risk_context_report.py",
    "ESMO2025/generate_homogeneity_report.py"
]

for f in files:
    p = Path(f)
    if not p.exists(): continue
    text = p.read_text('utf-8')
    text = re.sub(r"tracker\s*=\s*Tracker\(\)\n?tracker\.start\(\)\n?", "", text)
    text = re.sub(r'set_params\(\s*project_name=[^)]+\n\)\n?', '', text)
    
    p.write_text(text, 'utf-8')
    print(f"Fixed {f}")
