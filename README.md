# ----- README -----

@"
# FRED Economic Analysis
download GDP & Unemployment Rate from FRED, plot levels and Baxter–King cycles.

![Business-cycle plot](figures/bk_gdp_unrate.png)

## Quick start
`bash
python -m venv venv
venv\Scripts\activate           # PowerShell: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\analysis.py
mkdir src
