# Data

This project uses publicly available MLB Statcast data.

Pitch-level data is retrieved programmatically using the
`pybaseball` Python package.

Raw Statcast CSV files are not stored in this repository.
They can be reproduced using:

`src/download_data.py`

## Target Variable

The primary target variable is `whiff`.

- `1` = swinging strike
- `0` = all other pitch outcomes

## Potential Model Features

Features explored in this project include:

- Pitch type
- Release velocity
- Spin rate
- Horizontal movement
- Vertical movement
- Horizontal plate location
- Vertical plate location
- Release extension
- Ball-strike count
- Pitcher handedness
- Batter handedness
