
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Interactive Map Visualization",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# 2. LOAD NATURAL EARTH DATASET
# --------------------------------------------------

# Find the dataset relative to this Python file
BASE_DIR = Path(__file__).resolve().parent

SHAPEFILE_PATH = (
    BASE_DIR
    / "ne_110m_admin_0_countries"
    / "ne_110m_admin_0_countries.shp"
)

@st.cache_data
def load_data():

    if not SHAPEFILE_PATH.exists():
        raise FileNotFoundError(
            f"Shapefile not found: {SHAPEFILE_PATH}"
        )

    # Read shapefile
    gdf = gpd.read_file(SHAPEFILE_PATH)

    if gdf.empty:
        raise ValueError("The shapefile contains no data.")

    return gdf


# Load dataset with error handling
try:
    gdf = load_data()

except Exception as e:
    st.error("Unable to load the map dataset.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# 3. IDENTIFY COUNTRY AND POPULATION COLUMNS
# --------------------------------------------------

# Create case-insensitive column lookup
column_lookup = {
    str(col).lower(): col
    for col in gdf.columns
}

# Identify country name column
country_candidates = [
    "name",
    "admin",
    "name_en"
]

country_col = next(
    (
        column_lookup[col]
        for col in country_candidates
        if col in column_lookup
    ),
    None
)

if country_col is None:
    st.error("Country name column not found.")
    st.write(gdf.columns.tolist())
    st.stop()

# Identify population column
population_candidates = [
    "pop_est",
    "population"
]

population_col = next(
    (
        column_lookup[col]
        for col in population_candidates
        if col in column_lookup
    ),
    None
)

if population_col is None:
    st.error("Population column not found.")
    st.write(gdf.columns.tolist())
    st.stop()

# Standardise population column name
gdf["pop_est"] = pd.to_numeric(
    gdf[population_col],
    errors="coerce"
)


# --------------------------------------------------
# 4. PROJECTION OPTIONS
# --------------------------------------------------

projection_options = {
    "WGS 84 (Geographic)": "EPSG:4326",
    "Mercator": "EPSG:3395",
    "Web Mercator": "EPSG:3857",
    "Robinson": "+proj=robin +datum=WGS84 +units=m +no_defs",
    "Equal Earth": "+proj=eqearth +datum=WGS84 +units=m +no_defs",
    "Mollweide": "+proj=moll +datum=WGS84 +units=m +no_defs"
}


# --------------------------------------------------
# 5. APPLICATION TITLE AND NAVIGATION
# --------------------------------------------------

st.title("🌍 Interactive Map Visualization Examples")

st.write(
    "Explore map cosmetics, visual hierarchy, "
    "choropleth maps and geographical projections."
)

st.sidebar.header("Choose a Map Type")

map_type = st.sidebar.radio(
    "Select Map Type",
    [
        "Map Cosmetics",
        "Map Visual Hierarchy",
        "Choropleth Map",
        "Geo Projection"
    ]
)


# --------------------------------------------------
# 6. CALCULATE POPULATION DENSITY
# --------------------------------------------------

# Project the map to an equal-area coordinate system
# before calculating geographical area.

gdf_equal_area = gdf.to_crs("EPSG:6933")

area_km2 = (
    gdf_equal_area.geometry.area / 1_000_000
)

# Avoid division by zero
area_km2 = area_km2.replace(0, np.nan)

# Calculate population density
gdf["pop_density"] = (
    gdf["pop_est"] / area_km2
)

# Remove infinite values
gdf["pop_density"] = gdf["pop_density"].replace(
    [np.inf, -np.inf],
    np.nan
)


# --------------------------------------------------
# 7. MAP COSMETICS EXAMPLE
# --------------------------------------------------

if map_type == "Map Cosmetics":

    st.subheader("1. Map Cosmetics")

    st.write(
        "Customize the appearance of the map using "
        "different colours and background settings."
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    gdf.plot(
        ax=ax,
        color="skyblue",
        edgecolor="black",
        linewidth=0.5
    )

    ax.set_title(
        "Styled Map Example",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_facecolor("lightgrey")

    ax.set_axis_off()

    st.pyplot(fig)

    plt.close(fig)


# --------------------------------------------------
# 8. MAP VISUAL HIERARCHY EXAMPLE
# --------------------------------------------------

elif map_type == "Map Visual Hierarchy":

    st.subheader("2. Map Visual Hierarchy")

    st.write(
        "Select specific countries to highlight in red "
        "while keeping the remaining countries in sky blue."
    )

    default_countries = [
        "Brazil",
        "India",
        "China",
        "Australia",
        "South Africa",
        "Russia"
    ]

    available_countries = (
        gdf[country_col]
        .dropna()
        .tolist()
    )

    default_selection = [
        country
        for country in default_countries
        if country in available_countries
    ]

    highlighted_countries = st.multiselect(
        "Select countries to highlight in red",
        options=available_countries,
        default=default_selection
    )

    # Assign colours based on selection
    map_colors = gdf[country_col].apply(
        lambda country: (
            "red"
            if country in highlighted_countries
            else "skyblue"
        )
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    gdf.plot(
        color=map_colors,
        edgecolor="black",
        linewidth=0.5,
        ax=ax
    )

    ax.set_title(
        "Map Visual Hierarchy with Selected Countries Highlighted in Red",
        fontsize=13
    )

    ax.set_axis_off()

    st.pyplot(fig)

    plt.close(fig)

    st.write(
        f"Number of highlighted countries: "
        f"{len(highlighted_countries)}"
    )


# --------------------------------------------------
# 9. CHOROPLETH MAP EXAMPLE
# --------------------------------------------------

elif map_type == "Choropleth Map":

    st.subheader("3. Choropleth Map")

    st.write(
        "Visualize population density across countries "
        "using different colour schemes and logarithmic transformation."
    )

    color_choice = st.selectbox(
        "Choose Color Scheme",
        ["OrRd", "YlGn", "Blues", "Purples", "Greens"],
        index=0
    )

    use_log_scale = st.checkbox(
        "Use Log Transformation",
        value=True
    )

    plot_data = gdf.copy()

    if use_log_scale:

        plot_data["display_density"] = np.log1p(
            plot_data["pop_density"].clip(lower=0)
        )

    else:

        plot_data["display_density"] = (
            plot_data["pop_density"]
        )

    fig, ax = plt.subplots(figsize=(12, 7))

    plot_data.plot(
        column="display_density",
        cmap=color_choice,
        edgecolor="black",
        linewidth=0.4,
        legend=True,
        ax=ax,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        }
    )

    title_scale = (
        "Log Scale"
        if use_log_scale
        else "Original Scale"
    )

    ax.set_title(
        f"Population Density by Country "
        f"(Color Scheme: {color_choice}, {title_scale})",
        fontsize=13
    )

    ax.set_axis_off()

    st.pyplot(fig)

    plt.close(fig)

    st.caption(
        "Population density is calculated as estimated population "
        "per square kilometre. Log transformation helps reduce "
        "the effect of extremely high values."
    )


# --------------------------------------------------
# 10. GEO PROJECTION EXAMPLE
# --------------------------------------------------

elif map_type == "Geo Projection":

    st.subheader("4. Geo Projection")

    st.write(
        "Explore how different geographical projections "
        "change the appearance of the world map."
    )

    proj_choice = st.selectbox(
        "Select a Projection",
        list(projection_options.keys())
    )

    color_choice = st.selectbox(
        "Choose Color Scheme",
        ["OrRd", "YlGn", "Blues", "Purples", "Greens"],
        index=0
    )

    use_log_scale = st.checkbox(
        "Use Log Transformation for Population Density",
        value=True
    )

    plot_data = gdf.copy()

    if use_log_scale:

        plot_data["display_density"] = np.log1p(
            plot_data["pop_density"].clip(lower=0)
        )

    else:

        plot_data["display_density"] = (
            plot_data["pop_density"]
        )

    # Apply selected geographical projection
    gdf_proj = plot_data.to_crs(
        projection_options[proj_choice]
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    gdf_proj.plot(
        column="display_density",
        cmap=color_choice,
        edgecolor="black",
        linewidth=0.4,
        legend=True,
        ax=ax,
        missing_kwds={
            "color": "lightgrey",
            "label": "No data"
        }
    )

    ax.set_title(
        f"Map in {proj_choice} Projection",
        fontsize=14
    )

    ax.set_axis_off()

    st.pyplot(fig)

    plt.close(fig)

    st.info(
        f"Current projection: {proj_choice}"
    )


# --------------------------------------------------
# 11. DATASET INFORMATION
# --------------------------------------------------

with st.expander("View Dataset Information"):

    st.write(
        "Total countries:",
        len(gdf)
    )

    st.write("Dataset columns:")

    st.write(gdf.columns.tolist())

    st.write("Sample data:")

    st.dataframe(
        gdf[
            [
                country_col,
                "pop_est",
                "pop_density"
            ]
        ].head(10),
        use_container_width=True
    )


# --------------------------------------------------
# 12. SIDEBAR FOOTER
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.caption(
    "TFB3133/TEB3133 Data Visualization | Lab 7"
)
