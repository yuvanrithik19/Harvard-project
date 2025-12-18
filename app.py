
import asyncio
import aiohttp
import json
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from queries import SQL_QUERIES


# CONFIG

API_KEY = "f323a341-7fdc-497d-824f-fa94ff424e62"

DB_HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
DB_PORT = 4000
DB_NAME = "test"
DB_USER = "dBhZC2DneRLFSw9.root"
DB_PASSWORD = "cDwphfnAjgb810t1"

SSL_CA_PATH = r"C:\Users\Nirubhan\Downloads\harvard_project\isrgrootx1 (1).pem"

# DATABASE ENGINE
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    connect_args={"ssl": {"ca": SSL_CA_PATH}},
    future=True
)

# HARVARD API
BASE_URL = "https://api.harvardartmuseums.org/object"

async def fetch_harvard(api_key, classification, size=100, pages=5):
    meta, media, colors = [], [], []

    async with aiohttp.ClientSession() as session:
        for page in range(1, pages + 1):
            params = {
                "apikey": api_key,
                "classification": classification,
                "size": size,
                "page": page
            }

            async with session.get(BASE_URL, params=params) as resp:
                data = await resp.json()

            records = data.get("records", [])
            if not records:
                break

            for item in records:
                oid = item.get("id")

                meta.append({
                    "id": oid,
                    "title": item.get("title"),
                    "classification": item.get("classification"),
                    "culture": item.get("culture"),
                    "period": item.get("period"),
                    "century": item.get("century"),
                    "accessionyear": item.get("accessionyear"),
                    "department": item.get("department"),
                    "medium": item.get("medium"),
                })

                media.append({
                    "objectid": oid,
                    "mediacount": item.get("mediacount"),
                    "imagecount": item.get("imagecount"),
                    "colorcount": item.get("colorcount"),
                    "rank_d": item.get("rank"),
                    "datebegin": item.get("datebegin"),
                    "dateend": item.get("dateend"),
                })

                for c in item.get("colors") or []:
                    colors.append({
                        "objectid": oid,
                        "color": c.get("color"),
                        "hue": c.get("hue"),
                        "percent": c.get("percent"),
                    })

    return meta, media, colors

# STREAMLIT UI
st.set_page_config("Harvard Artifacts", layout="wide")
st.title("🏛 Harvard Artifacts Explorer")

classification = st.selectbox(
    "Select Classification",
    ["Prints", "Fragments", "Seals"]
)

# SESSION STATE 
if "data" not in st.session_state:
    st.session_state.data = {"meta": [], "media": [], "colors": []}

if "show_tables" not in st.session_state:
    st.session_state.show_tables = False

#  BUTTONS VISIBLE FROM START 
col1, col2 = st.columns(2)
btn_collect = col1.button("Collect Data")
btn_migrate = col2.button("Migrate to SQL")

#  COLLECT DATA 
if btn_collect:
    with st.spinner("Fetching data..."):
        meta, media, colors = asyncio.run(fetch_harvard(API_KEY, classification))
    st.session_state.data = {
        "meta": meta,
        "media": media,
        "colors": colors
    }
    st.success("Data collected successfully!")

#  JSON DISPLAY 
if st.session_state.data["meta"]:
    st.markdown("---")
    st.header("💾 Collected Data (JSON Preview)")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("📌 Metadata JSON")
        st.json(st.session_state.data["meta"])
        st.download_button(
            "⬇ Download Metadata JSON",
            json.dumps(st.session_state.data["meta"], indent=2),
            file_name="metadata.json",
            mime="application/json"
        )

    with c2:
        st.subheader("🖼 Media JSON")
        st.json(st.session_state.data["media"])
        st.download_button(
            "⬇ Download Media JSON",
            json.dumps(st.session_state.data["media"], indent=2),
            file_name="media.json",
            mime="application/json"
        )

    with c3:
        st.subheader("🎨 Colors JSON")
        st.json(st.session_state.data["colors"])
        st.download_button(
            "⬇ Download Colors JSON",
            json.dumps(st.session_state.data["colors"], indent=2),
            file_name="colors.json",
            mime="application/json"
        )

#  MIGRATE TO SQL (TABLE VIEW)
if btn_migrate and st.session_state.data["meta"]:
    st.session_state.show_tables = True

# TABLE DISPLAY
if st.session_state.show_tables:
    st.markdown("---")
    st.header("📊 Collected Data (Table View)")
    tab1, tab2, tab3 = st.tabs(["Metadata", "Media", "Colors"])

    with tab1:
        df_meta = pd.DataFrame(st.session_state.data["meta"])
        st.dataframe(df_meta, use_container_width=True)

    with tab2:
        df_media = pd.DataFrame(st.session_state.data["media"])
        st.dataframe(df_media, use_container_width=True)

    with tab3:
        df_colors = pd.DataFrame(st.session_state.data["colors"])
        st.dataframe(df_colors, use_container_width=True)

if st.session_state.data["meta"]:
    st.markdown("---")
    st.header("🔍 SQL Queries")

    selected_query = st.selectbox(
        "Choose a Query",
        list(SQL_QUERIES.keys())
    )

    params = {}
    if selected_query.startswith("16."):
        params["id"] = st.text_input("Enter Artifact ID")

    if st.button("Execute Query"):
        with engine.connect() as conn:
            df = pd.read_sql(text(SQL_QUERIES[selected_query]), conn, params=params)
        st.dataframe(df, use_container_width=True)
