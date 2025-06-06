# libraries:
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web
from statsmodels.tsa.filters import bkfilter
import pathlib 

SERIES = [\"GDP\", \"UNRATE\"]
START  = \"2000-01-01\"

df = web.DataReader(SERIES, \"fred\", START)

# Convert UNRATE monthly → quarterly average
df_q = df.copy()
df_q[\"UNRATE\"] = df[\"UNRATE\"].resample(\"Q\").mean()

# Baxter–King filter (6-32 quarters, K=12)
gdp_cycle = bkfilter(df_q[\"GDP\"],    low=6, high=32, K=12)
unr_cycle = bkfilter(df_q[\"UNRATE\"], low=6, high=32, K=12)
cycle_df  = pd.DataFrame({\"GDP_cycle\": gdp_cycle,
                          \"UNRATE_cycle\": unr_cycle})

# Plot
fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True)
df_q[["GDP", "UNRATE"]].plot(ax=axes[0])
axes[0].set_title("Levels (quarterly)")
cycle_df.plot(ax=axes[1])
axes[1].set_title("Baxter–King Cycles (6–32 qtrs)")
plt.tight_layout()

pathlib.Path("figures").mkdir(exist_ok=True)    # make dir
outfile = "figures/bk_gdp_unrate.png"          
plt.savefig(outfile, dpi=300)
print(f"✅  Plot saved as {outfile}")
