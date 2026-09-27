"""
Streamlit activity - Water Resources in Lebanon (2023)
Builds on the Plotly assignment: same dataset, two related visualizations,
now made interactive with two LINKED widgets (area selection drives which
towns are available to drill into).
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_prep import COLS, load_data

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Lebanon Water Resources Explorer",
    page_icon="💧",
    layout="wide",
)

GOOD, ACCEPT, BAD = "#2ca02c", "#f2c744", "#d62728"

df = load_data()

# ----------------------------------------------------------------------
# Header / context
# ----------------------------------------------------------------------
st.title("💧 Water Resources in Lebanon (2023)")
st.markdown(
    """
This page explores the condition of the public water network and the
availability of natural springs across Lebanon's towns, using the 2023
**Water Resources** dataset published on
[linked.aub.edu.lb](https://linked.aub.edu.lb:8502/) (Impact Open Data /
CODEC Lebanon). The dataset covers **1,137 towns** and reports, for each
one, the condition of its water network (good / acceptable / bad), its
main potable water sources, and its number of permanent and seasonal
springs.

Use the controls below to compare areas, then drill into a single town.
"""
)

st.divider()

# ----------------------------------------------------------------------
# WIDGET 1 - Area multiselect (drives everything downstream)
# ----------------------------------------------------------------------
area_counts = df["Area"].value_counts()
all_areas = area_counts.index.tolist()
default_areas = area_counts.head(6).index.tolist()  # 6 most-surveyed areas, for a readable default

st.subheader("1. Choose areas to compare")
selected_areas = st.multiselect(
    "Governorates / districts",
    options=all_areas,
    default=default_areas,
    help="Filters both charts below, and the list of towns you can drill into.",
)

if not selected_areas:
    st.warning("Select at least one area to see the charts.")
    st.stop()

area_df = df[df["Area"].isin(selected_areas)].copy()

# ----------------------------------------------------------------------
# Chart 1 - stacked bar of network condition by area
# ----------------------------------------------------------------------
state_by_area = (
    area_df.groupby("Area")[[COLS["good"], COLS["acceptable"], COLS["bad"]]]
    .sum()
    .rename(columns={COLS["good"]: "Good", COLS["acceptable"]: "Acceptable", COLS["bad"]: "Bad"})
)
state_by_area = state_by_area.loc[state_by_area.sum(axis=1).sort_values(ascending=False).index]
state_by_area_long = state_by_area.reset_index().melt(id_vars="Area", var_name="Condition", value_name="Towns")

fig1 = px.bar(
    state_by_area_long,
    x="Area",
    y="Towns",
    color="Condition",
    barmode="stack",
    category_orders={"Condition": ["Good", "Acceptable", "Bad"]},
    color_discrete_map={"Good": GOOD, "Acceptable": ACCEPT, "Bad": BAD},
    title="Water network condition, by area",
)
fig1.update_layout(xaxis_title="Area", yaxis_title="Number of towns", legend_title="Condition")

col1, col2 = st.columns([3, 2])
with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    total_towns = int(state_by_area.values.sum())
    bad_share = state_by_area["Bad"].sum() / total_towns * 100 if total_towns else 0
    worst_area = state_by_area["Bad"].idxmax()
    st.metric("Towns in selected areas", total_towns)
    st.metric("Share with a 'bad' network", f"{bad_share:.0f}%")
    st.metric("Worst area (most 'bad' towns)", worst_area)
    st.markdown(
        f"**Insight:** Within your current selection, **{worst_area}** has the most towns "
        f"reporting a bad network. Network condition is uneven across areas rather than "
        f"uniformly poor or uniformly good — adjust the selection above to see how the "
        f"picture changes as you add or remove areas."
    )

st.divider()

# ----------------------------------------------------------------------
# WIDGET 2 - Town selectbox, OPTIONS DEPEND ON WIDGET 1 (the link)
# ----------------------------------------------------------------------
st.subheader("2. Drill into a town")

towns_in_selection = sorted(area_df["Town"].dropna().unique().tolist())
selected_town = st.selectbox(
    "Town (only towns from the areas selected above are listed)",
    options=towns_in_selection,
    help="This list updates automatically to only show towns inside the areas you picked above.",
)

town_row = area_df[area_df["Town"] == selected_town].iloc[0]

# ----------------------------------------------------------------------
# Chart 2 - scatter of permanent vs seasonal springs, selected town highlighted
# ----------------------------------------------------------------------
fig2 = px.scatter(
    area_df,
    x=COLS["perm_springs"],
    y=COLS["seasonal_springs"],
    color="Area",
    opacity=0.55,
    hover_name="Town",
    title="Permanent vs. seasonal water springs per town",
)
fig2.add_trace(
    go.Scatter(
        x=[town_row[COLS["perm_springs"]]],
        y=[town_row[COLS["seasonal_springs"]]],
        mode="markers+text",
        marker=dict(size=18, color="black", symbol="star"),
        text=[selected_town],
        textposition="top center",
        name=f"Selected: {selected_town}",
    )
)
fig2.update_layout(xaxis_title="Permanent springs", yaxis_title="Seasonal springs")

col3, col4 = st.columns([3, 2])
with col3:
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    corr = area_df[COLS["perm_springs"]].corr(area_df[COLS["seasonal_springs"]])
    condition = (
        "Good" if town_row[COLS["good"]] == 1 else "Acceptable" if town_row[COLS["acceptable"]] == 1 else "Bad"
        if town_row[COLS["bad"]] == 1 else "Not reported"
    )
    st.markdown(f"#### {selected_town}")
    st.write(f"**Area:** {town_row['Area']}")
    st.write(f"**Network condition:** {condition}")
    st.write(f"**Permanent springs:** {int(town_row[COLS['perm_springs']])}")
    st.write(f"**Seasonal springs:** {int(town_row[COLS['seasonal_springs']])}")
    st.markdown(
        f"**Insight:** Across the selected areas, permanent and seasonal springs are "
        f"moderately correlated (r = {corr:.2f}) — towns rich in one tend to have more of "
        f"the other, likely reflecting shared terrain. {selected_town} is highlighted above "
        f"so you can see exactly where it sits relative to that pattern."
    )

st.divider()

# ----------------------------------------------------------------------
# Design justifications
# ----------------------------------------------------------------------
st.subheader("Design justifications")

with st.expander("Why a multiselect for area comparison?"):
    st.markdown(
        """
**User question it answers:** *"How does water infrastructure differ across the
regions I care about?"* Readers rarely want all 25 areas at once — that many
stacked bars becomes unreadable — but they do want to compare more than one
area side by side.

**Why this widget instead of an alternative:** I considered a single
dropdown (one area at a time) and a row of checkboxes (one per area). A
single dropdown can't support comparison, which is the whole point of
Chart 1. Checkboxes would work but don't scale to 25 areas without
consuming the whole page. `st.multiselect` lets the reader pick exactly
the areas they want to compare, with a searchable list, in one compact
widget.

**Course concept:** this is about **reducing clutter to focus attention**.
Filtering down to a handful of areas removes chart elements that aren't
relevant to the reader's current question, so the remaining bars are easier
to compare and the pattern (which areas are worst-off) stands out instead
of being buried in 25 bars.
"""
    )

with st.expander("Why a linked selectbox to drill into a single town?"):
    st.markdown(
        """
**User question it answers:** *"I can see area X has a lot of 'bad' network
towns — but which town, specifically, and how does its spring access
compare to its neighbors?"* The area-level chart can't answer a question
about one specific place.

**Why this widget instead of an alternative:** I considered a free-text
search box and a slider over an alphabetical town index. Free text risks
typos and doesn't show the reader what's available. A slider implies an
order that towns don't have (they're categorical, not numeric). A
`st.selectbox` restricted to the *currently selected areas* — rather than
all 1,137 towns — keeps the list short, relevant, and impossible to
misuse: a reader can never accidentally select a town outside the region
they're studying.

**Course concept:** this demonstrates **providing context while focusing
attention** (and a simple form of linked/coordinated views): the scatter
plot keeps every town from the selected areas visible as context, while
the selected town is highlighted as a distinct marker on top of that
same chart, so the reader sees the individual case *and* where it falls
relative to the broader pattern at the same time. This is also the link
between the two interaction features: Widget 1's output (the set of
areas) becomes Widget 2's input (the list of selectable towns), so the
reader drills down through one connected decision rather than filtering
two unrelated things.
"""
    )

st.divider()
st.caption(
    "Data: Water Resources - Lebanon 2023, linked.aub.edu.lb Open Data "
    "(Impact Open Data / CODEC Lebanon). Built with Streamlit + Plotly."
)
