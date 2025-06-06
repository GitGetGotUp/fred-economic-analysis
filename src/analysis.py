"""
Baxter King (BK) filter demo on FRED data
Creates figures/bk_gdp_unrate.png with clearly visible lines
"""

from datetime import datetime
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.bk_filter import bkfilter
from fredapi import Fred

# ────────────────────────────────
#  1. Download data via fredapi
# ────────────────────────────────
fred = Fred(api_key="3f8e92e5cfc9b253a12a0fd0610576ef")

df = pd.DataFrame({
    "GDP": fred.get_series("GDP",    observation_start="2000-01-01"),
    "UNRATE": fred.get_series("UNRATE", observation_start="2000-01-01")
})

# Convert monthly UNRATE to a quarterly average
df_q = df.copy()
df_q["UNRATE"] = df["UNRATE"].resample("Q").mean()

# ────────────────────────────────
#  2. Baxter–King filter (6–32 qtrs)
# ────────────────────────────────

df_qtr = pd.DataFrame({
    "GDP":    df["GDP"].resample("Q").last(),   
    "UNRATE": df["UNRATE"].resample("Q").mean()  #average out
}).dropna() 

gdp_cycle = bkfilter(df_qtr["GDP"],    low=6, high=32, K=12)  
unr_cycle = bkfilter(df_qtr["UNRATE"], low=6, high=32, K=12)  
cycle_df  = pd.DataFrame({"GDP_cycle": gdp_cycle,
                          "UNRATE_cycle": unr_cycle})
# ────────────────────────────────
#  3. Plot
# ────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

# Levels
ax1.plot(df_q.index, df_q["GDP"],    linewidth=1.8, marker="o",
         label="GDP (bil.$)")
ax1b = ax1.twinx()
ax1b.plot(df_q.index, df_q["UNRATE"], linewidth=1.8, color="firebrick",
          label="UNRATE (%)")
ax1.set_title("GDP and Unemployment Rate – levels")
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax1b.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="upper left")

# Cycles
ax2.plot(cycle_df.index, cycle_df["GDP_cycle"],
         linewidth=1.6, label="GDP cycle")
ax2.plot(cycle_df.index, cycle_df["UNRATE_cycle"],
         linewidth=1.6, color="firebrick", label="UNRATE cycle")
ax2.axhline(0, color="gray", linewidth=0.8)
ax2.set_title("Baxter–King cycles (6–32 quarters)")
ax2.legend()

plt.tight_layout()

# ────────────────────────────────
#  4. Save
# ────────────────────────────────
pathlib.Path("figures").mkdir(exist_ok=True)
outfile = "figures/bk_gdp_unrate.png"
plt.savefig(outfile, dpi=300) 
plt.close()
print(f"Plot saved as {outfile}")
