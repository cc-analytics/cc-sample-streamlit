import streamlit as st
import streamlit.components.v1 as components
from streamlit.hello.utils import show_code
from urllib.error import URLError

import altair as alt
import pandas as pd

# embed streamlit docs in a streamlit app
st.set_page_config(page_title="Snowflake Demo", page_icon="❄️")
st.title("Snowflake Connectivity")
st.markdown("#### Connect to data from my Snowflake Database")

st.markdown("##### url: https://tinyurl.com/4zv2fhc6")
st.image("online_sales_D3_ChrisChen.png")
st.sidebar.markdown("##### Created by:")
st.sidebar.markdown("# Chris Chen")
st.sidebar.markdown("## Seasoned Data Analytics Professional")
st.sidebar.markdown("chrischen.analytics@gmail.com")
st.sidebar.markdown("https://www.linkedin.com/in/chrischenanalytics")

st.set_page_config(layout="wide")

def init_connection():
    return snowflake.connector.connect(
        user=st.secrets["connections"]["snowflake"]["user"],
        password=st.secrets["connections"]["snowflake"]["password"],
        account=st.secrets["connections"]["snowflake"]["account"],
        warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
        database=st.secrets["connections"]["snowflake"]["database"],
        schema=st.secrets["connections"]["snowflake"]["schema"]
    )

conn = init_connection()

# Function to query data from Snowflake
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()
    
@st.cache_data
def load_customer():
    results = run_query("SELECT B.N_NAME as COUNTRY, A.C_MKT_SEGMENT as Segment, SUM(A.C_ACCTBAL) as Balance from CUSTOMER A LEFT JOIN NATION B ON A.C_NATIONKEY = B.N_NATIONKEY group by B.N_NAME, A.C_MKT_SEGMENT ")
    return results.set_index("N_NAME")

# try:
if st.button("Show Acct Balance by Segment"):      
    df = load_customer()
    st.dataframe(df)
