from pathlib import Path

import pandas as pd
from pybaseball import statcast


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

START_DATE = "2025-04-01"
END_DATE = "2025-04-07"

DATA_PATH = Path("data/statcast_2025_sample.csv")


# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

def download_statcast_data(start_date, end_date):
    """
    Download MLB pitch-level Statcast data.

    Parameters
    ----------
    start_date : str
        Beginning of date range in YYYY-MM-DD format.

    end_date : str
        End of date range in YYYY-MM-DD format.

    Returns
    -------
    pandas.DataFrame
        Pitch-level Statcast data.
    """

    print(
        f"Downloading Statcast data "
        f"from {start_date} through {end_date}..."
    )

    data = statcast(
        start_dt=start_date,
        end_dt=end_date
    )

    print(f"Downloaded {len(data):,} pitches.")

    return data


# --------------------------------------------------
# CREATE TARGET
# --------------------------------------------------

def create_whiff_target(data):
    """
    Create the target variable for our model.

    whiff = 1 if the pitch produced a swinging strike
    whiff = 0 otherwise
    """

    whiff_descriptions = [
        "swinging_strike",
        "swinging_strike_blocked"
    ]

    data = data.copy()

    data["whiff"] = (
        data["description"]
        .isin(whiff_descriptions)
        .astype(int)
    )

    return data


# --------------------------------------------------
# BASIC DATA CHECK
# --------------------------------------------------

def inspect_data(data):

    print("\n----------------------------")
    print("DATASET INFORMATION")
    print("----------------------------")

    print(f"\nRows: {len(data):,}")
    print(f"Columns: {len(data.columns)}")

    print("\nPitch types:")
    print(data["pitch_type"].value_counts().head(10))

    print("\nWhiff distribution:")
    print(data["whiff"].value_counts())

    print("\nWhiff rate:")
    print(f"{data['whiff'].mean():.2%}")


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

def save_data(data, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        path,
        index=False
    )

    print(f"\nData saved to: {path}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    data = download_statcast_data(
        START_DATE,
        END_DATE
    )

    data = create_whiff_target(data)

    inspect_data(data)

    save_data(
        data,
        DATA_PATH
    )


if __name__ == "__main__":
    main()
