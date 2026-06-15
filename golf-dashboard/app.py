import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Svenska Golfklubbar", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/courses_with_coords.csv")
    return df

df = load_data()

st.title("🏌️ Svenska Golfklubbar")
st.markdown(f"Visar **{len(df)}** klubbar från golf.se")

# --- Sidebar filter ---
st.sidebar.header("Filtrera")
cities = sorted(df['city'].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Stad", ["Alla"] + cities)
search = st.sidebar.text_input("Sök klubbnamn")

# --- Filtrera data ---
filtered = df.copy()
if selected_city != "Alla":
    filtered = filtered[filtered['city'] == selected_city]
if search:
    filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]

st.markdown(f"### {len(filtered)} klubbar matchar")

# --- Karta ---
map_data = filtered.dropna(subset=['lat', 'lng'])
if not map_data.empty:
    fig = px.scatter_map(
        map_data,
        lat="lat",
        lon="lng",
        hover_name="name",
        hover_data={"city": True, "lat": False, "lng": False},
        zoom=4,
        center={"lat": 62, "lon": 16},
        height=500,
        map_style="open-street-map"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tabell ---
st.dataframe(
    filtered[['name', 'city', 'email']].reset_index(drop=True),
    use_container_width=True
)