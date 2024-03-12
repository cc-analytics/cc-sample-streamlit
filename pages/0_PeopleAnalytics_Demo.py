import streamlit as st
import streamlit.components.v1 as components
from streamlit.hello.utils import show_code
import snowflake.connector
from urllib.error import URLError

import altair as alt
import pandas as pd

# embed streamlit docs in a streamlit app
st.set_page_config(page_title="People Analytics Demo", page_icon="🧑", layout="wide")
st.title("People Analytics Demo")
st.sidebar.markdown("##### Created by:")
st.sidebar.markdown("# Chris Chen")
st.sidebar.markdown("## Seasoned Data Analytics Professional")
st.sidebar.markdown("chrischen.analytics@gmail.com")
st.sidebar.markdown("https://www.linkedin.com/in/chrischenanalytics")

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
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetch_pandas_all()
    
# @st.cache_data
# def load_country_segment():
#     results = run_query("SELECT B.N_NAME as COUNTRY, A.C_MKTSEGMENT as Segment, SUM(A.C_ACCTBAL) as Balance from CUSTOMER A LEFT JOIN NATION B ON A.C_NATIONKEY = B.N_NATIONKEY group by B.N_NAME, A.C_MKTSEGMENT ")
#     # return results.set_index("N_NAME")
#     return results

# def load_segment():
#     results = run_query("SELECT A.C_MKTSEGMENT as Segment, SUM(A.C_ACCTBAL) as Balance from CUSTOMER A  group by  A.C_MKTSEGMENT ")
#     # return results.set_index("N_NAME")
#     return results
# df = None
# # try:

# with st.container():
#     bt1 = st.button("Show Acct Balance by Country, Segment")
#     bt2 = st.button("Show Acct Balance by Segment")

# with st.container():
#     row = st.columns(2)
#     if bt1:
#         df = load_country_segment()
#         st.dataframe(df)
#     elif bt2:
#         df = load_segment()    
#         row[0].bar_chart(df, x="SEGMENT", y="BALANCE")
#         row[1].dataframe(df)
