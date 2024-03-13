import streamlit as st
import streamlit.components.v1 as components
from streamlit_pills import pills
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

tabMain, tabInfo, tabTo_dos = st.tabs(["Main", "Info", "To-do's"])

with tabMain:

    st.write("")

    c30, c31, c32 = st.columns([0.2, 0.1, 3])

    st.subheader("Select Topic:")

    example = pills(
        "",
        [
            "Overview",
            "Employee Retention",
            "Recruitment",
        ],
        [
            "📊",
            "📈",
            "💼",
        ],
        label_visibility="collapsed",
    )

with tabInfo:
    st.write("")
    st.write("")
    st.subheader(" Streamlit App Demo")    
    st.markdown(
    """This Streamlit app connects to my Snowflake data tables.  The mock-up values are created by OpenAI's GPT-4.  Cache is implemented so it does not hit the tables every time (to save my wallet 😄).
    Then it does the calculations in Python and display the charts.  It shows how you can use Streamlit to build a dashboard.
    I will include my sample app in Tableau, too."""
)
    st.write("")
    st.subheader(" What is People Analytics?")
    st.markdown(
        """People Analytics is the data-driven approach to managing people at work. By leveraging data analysis, statistics, and technology, it aims to improve decision-making, enhance employee experience, and boost organizational performance. It covers areas like recruitment, performance evaluation, leadership development, and employee retention, turning insights into actionable strategies.
"""
    )
    st.write("")
    st.subheader("🎈 What is Streamlit?")
    st.markdown(
        "[Streamlit](https://streamlit.io) is an open-source Python library that allows users to create interactive, web-based data visualization and machine learning applications without the need for extensive web development knowledge"
    )

    st.write("---")

    st.subheader("📖 Resources")
    st.markdown(
        """
    - OpenAI
        - [OpenAI Playground](https://beta.openai.com/playground)
        - [OpenAI Documentation](https://beta.openai.com/docs)    
    - Streamlit
        - [Documentation](https://docs.streamlit.io/)
        - [Gallery](https://streamlit.io/gallery)
        - [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
        - [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
        - Deploy your apps using [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks 
    """)

with tabTo_dos:
    with st.expander("To-do", expanded=True):
        st.write(
            """
        - Deploy the chart component
        - Add a link to the Tableau version
        """
        )
        st.write("")
    with st.expander("Done", expanded=True):
        st.write(
            """
        - Include information in the 'Info' tab.
        - Set up app layout.
        - Create Snowflake tables.
        - Populate mock-up data gnerated by GPT-4.
        - Create People Analytics metrics.

        """
        )
        st.write("")

conn = init_connection()

# Function to query data from Snowflake
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetch_pandas_all()
    
# @st.cache_data
def load_people_data():
    results = run_query("SELECT B.N_NAME as COUNTRY, A.C_MKTSEGMENT as Segment, SUM(A.C_ACCTBAL) as Balance from CUSTOMER A LEFT JOIN NATION B ON A.C_NATIONKEY = B.N_NATIONKEY group by B.N_NAME, A.C_MKTSEGMENT ")
    # return results.set_index("N_NAME")
    return results

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

