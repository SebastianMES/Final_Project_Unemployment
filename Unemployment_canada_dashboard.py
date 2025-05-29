import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("Canadian Employment Dashboard")
st.write("""
This interactive dashboard shows employment trends across Canadian provinces by age group.
You can filter by province, year range, age group and the employment metric you want to know about.
""")

df = pd.read_csv(r"C:\Users\car_f\JupyterNotebook\Unemployment_Final_Proj\Final_Project_Unemployment\Unemployment_clean.csv")
df['REF_DATE'] = pd.to_datetime(df['REF_DATE']) # change to date time 'REF_DATE'

if st.checkbox("Show DataFrame"):
     # show dataframe
    st.dataframe(df)

# Sidebar: Filters
st.sidebar.header("Filters")

## Province
provinces = sorted(df['GEO'].unique())
selected_province = st.sidebar.selectbox("Select Province", provinces)

## age group
age_groups = sorted(df['Age_group'].unique())
selected_age = st.sidebar.selectbox("Select Age Group", age_groups)

## years range
min_year = int(df['REF_DATE'].dt.year.min())
max_year = int(df['REF_DATE'].dt.year.max())
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (2010, 2022))

# visualization metrics
metrics = [
    'Unemployment_rate',
    'Employment_rate',
    'Participation_rate',
    'Employment',
    'Unemployment',
    'Labour_force',
    'Fulltime_employment',
    'Parttime_employment'
]
selected_metric = st.sidebar.selectbox("Select Metric to Visualize", metrics)

# Dataframe Filter for both graphs
filtered_df = df[
    (df['Age_group'] == selected_age) &
    (df['REF_DATE'].dt.year.between(*selected_years))
]

# Filter for line plot
line_df = filtered_df[filtered_df['GEO'] == selected_province]

#
title_replace_metric = selected_metric.replace('_', ' ').title()

# Line graph for Unemployment rate
st.subheader(f"{title_replace_metric} Over Time - {selected_age}")
fig_line = px.line(
    line_df,
    x='REF_DATE',
    y=selected_metric,
    title=f"{title_replace_metric} per Province Over Time",
    labels={'REF_DATE': 'Date', selected_metric: title_replace_metric}
)
st.plotly_chart(fig_line, use_container_width=True)

#interactive map
## last date range
latest_date = filtered_df['REF_DATE'].max()
map_data = filtered_df[filtered_df['REF_DATE'] == latest_date]

# load GeoJSON
with open(r"/Unemployment_project/Final_Project_Unemployment/canada.geojson", "r") as file:
    geojson = json.load(file)

st.subheader(f"Map for {title_replace_metric} - {selected_age} on {latest_date.strftime('%B %Y')}")

# map
fig_map = px.choropleth(
    map_data,
    geojson=geojson,
    locations='GEO',
    featureidkey="properties.name",
    color=selected_metric,
    hover_name='GEO',
    hover_data={
        selected_metric: ':.2f',
        'REF_DATE': True,
        'Age_group': True
    },
    color_continuous_scale='Reds',
    scope='north america'
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)