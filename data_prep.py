"""
Shared data preparation for the Lebanon Water Resources (2023) dataset.
Source: linked.aub.edu.lb Open Data (Impact Open Data / CODEC Lebanon)

Reused as-is from the Plotly assignment so the Streamlit app stays
consistent with the earlier deliverable.
"""
import pandas as pd

RAW_PATH = "water_resources_lebanon2023.csv"

AREA_FIXES = {
    "Miniyehâ\x80\x93Danniyeh": "Minieh-Danniyeh",
    "ZahlÃ©": "Zahle",
    "Tripoli, Lebanon": "Tripoli",
}

COLS = {
    "good": "State of the water network - good",
    "acceptable": "State of the water network - acceptable",
    "bad": "State of the water network - bad",
    "public_network": "Potable water source - public network",
    "artesian_well": "Potable water source - artesian well",
    "gallons": "Potable water source - gallons purchase",
    "water_point": "Potable water source - water point",
    "other_source": "Potable water source - other",
    "perm_springs": "Total number of permanent water springs",
    "seasonal_springs": "Total number of seasonal water springs",
    "seasonal_points": "Total number of seasonal water points",
}


def load_data(path: str = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

    area = df["refArea"].str.extract(r"/([^/]+)$")[0].str.replace("_", " ", regex=False)
    area = area.str.replace(" Governorate", "", regex=False).str.replace(" District", "", regex=False)
    area = area.replace(AREA_FIXES)
    df["Area"] = area

    return df
