from pybaseball import statcast
import pandas as pd
from pathlib import Path
import time

# -----------------------------------------
# Configuration
# -----------------------------------------

START_DATE = "2025-03-27"
END_DATE = "2025-09-28"

OUTPUT_PATH = Path("data/statcast_2025_full.csv")

# Download approximately one month at a time
date_ranges = [
    ("2025-03-27", "2025-04-30"),
    ("2025-05-01", "2025-05-31"),
    ("2025-06-01", "2025-06-30"),
    ("2025-07-01", "2025-07-31"),
    ("2025-08-01", "2025-08-31"),
    ("2025-09-01", "2025-09-28"),
]

all_data = []

print("Downloading 2025 MLB Statcast data...")
print()

for start_date, end_date in date_ranges:

    print(
        f"Downloading {start_date} through {end_date}..."
    )

    chunk = statcast(
        start_dt=start_date,
        end_dt=end_date
    )

    print(
        f"Downloaded {len(chunk):,} pitches."
    )

    all_data.append(chunk)

    # Be polite to the data source
    time.sleep(2)

print()
print("Combining datasets...")

data = pd.concat(
    all_data,
    ignore_index=True
)

print(f"Total pitches: {len(data):,}")
print(f"Columns: {len(data.columns)}")

# -----------------------------------------
# Create whiff target
# -----------------------------------------

whiff_descriptions = [
    "swinging_strike",
    "swinging_strike_blocked"
]

data["whiff"] = (
    data["description"]
    .isin(whiff_descriptions)
    .astype(int)
)

print(
    f"Total whiffs: {data['whiff'].sum():,}"
)

print(
    f"Overall whiff rate: {data['whiff'].mean():.2%}"
)

# -----------------------------------------
# Save
# -----------------------------------------

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

data.to_csv(
    OUTPUT_PATH,
    index=False
)

print()
print(
    f"Saved full dataset to {OUTPUT_PATH}"
)
