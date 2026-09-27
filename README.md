# Lebanon Water Resources Explorer

An interactive Streamlit page exploring the condition of the water network
and spring availability across Lebanese towns, built on the 2023 Water
Resources dataset from [linked.aub.edu.lb](https://linked.aub.edu.lb:8502/)
(Impact Open Data / CODEC Lebanon).

**Live app:** _add your Streamlit Community Cloud link here after deploying_

## What it does

- **Chart 1** — stacked bar chart of water network condition (good /
  acceptable / bad) by area.
- **Chart 2** — scatter plot of permanent vs. seasonal water springs per
  town.
- **Linked interactivity:**
  1. A multiselect lets you choose which areas (governorates/districts) to
     compare — this filters both charts.
  2. A selectbox lets you drill into one town — but its options are
     restricted to only the towns inside the areas you picked in step 1,
     so the two widgets are linked rather than independent.

## Files

| File | Purpose |
|---|---|
| `app.py` | Streamlit app |
| `data_prep.py` | Loads and cleans the CSV (shared with the earlier Plotly assignment) |
| `water_resources_lebanon2023.csv` | Dataset |
| `requirements.txt` | Python dependencies |

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and click **New app**.
3. Pick the repo, branch, and set the main file path to `app.py`.
4. Click **Deploy**. The first build installs everything in
   `requirements.txt`.
5. Copy the public URL Streamlit gives you into this README and your
   Moodle submission.

## Data source

Water Resources — Lebanon (2023), published on linked.aub.edu.lb Open Data
(Impact Open Data / CODEC Lebanon).
