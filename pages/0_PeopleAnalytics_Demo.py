import streamlit as st
import streamlit.components.v1 as components
from streamlit_pills import pills
# ----------------------Importing utils.py----------------------
import io
from utils import (
    init_connection,
    run_query,
    show_code
)

from urllib.error import URLError

import altair as alt
import pandas as pd

@st.cache_data
def load_people_data():
    results = run_query("SELECT A.EMPLOYEE_ID, A.NAME, A.BIRTH_DATE, A.\"Education\", A.HIRED_DATE, A.JOB_NAME, A.DEPARTMENT_NAME, B.\"Division\" as DIVISION_NAME from CCMOCKUP.PUBLIC.EMPLOYEE_TEST A join CCMOCKUP.PUBLIC.DEPARTMENT_TEST B on A.DEPARTMENT_NAME = B.\"Department\"")
    return results

st.set_page_config(page_title="People Analytics Demo", page_icon="🧑", layout="wide")
st.title("People Analytics Demo")
st.sidebar.markdown("##### Created by:")
st.sidebar.markdown("# Chris Chen")
st.sidebar.markdown("## Seasoned Data Analytics Professional")
st.sidebar.markdown("chrischen.analytics@gmail.com")
st.sidebar.markdown("https://www.linkedin.com/in/chrischenanalytics")

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
            "Recruitment"
        ],
        [
            "📊",
            "📈",
            "💼"
        ],
        label_visibility="collapsed"
    )
    submitted = st.button("Run!")
    if submitted:
        df = load_people_data()
        if example == "Overview":
            # Generating the count of records with 'hired_date' greater than each date
            st.markdown("### Total Headcount: ")
            total_Count = df['HIRED_DATE'].count()
            st.write(total_Count)            
            counts = df['HIRED_DATE'].value_counts().sort_index().cumsum()[::-1]
            counts_df = pd.DataFrame({
                'Hired Date': counts.index,
                'Cumulative Count': counts.values
            })
            # Group by 'HIRED_DATE' and count occurrences
            hiring_counts_df = df.groupby('HIRED_DATE')['HIRED_DATE'].count().reset_index(name='Count')

            # Renaming the 'Value' column to 'Count' to better reflect the new content
            hiring_counts_df = hiring_counts_df.rename(columns={'Value': 'Count'})

            row1 =  st.columns(2, gap="small")
            with row1[0]:
                st.write("Cumulative Head Count")
                chart = st.line_chart(counts_df.set_index('Hired Date'),width=200, height=260)
            with row1[1]:
                st.write("Historical Hiring")
                chart = st.line_chart(hiring_counts_df.set_index('HIRED_DATE'),width=200, height=260)
            row2 = st.columns(2, gap="small")
            with row2[0]:
                st.write("Head Count by Division")
                counts_by_division_df = df.groupby('DIVISION_NAME')['DIVISION_NAME'].count().reset_index(name='Count')
                bar_chart = st.bar_chart(data=counts_by_division_df,x='DIVISION_NAME')
            with row2[1]:
                st.write("Head Count by Department")
                counts_by_division_df = df.groupby('DEPARTMENT_NAME')['DEPARTMENT_NAME'].count().reset_index(name='Count')
                bar_chart = st.bar_chart(data=counts_by_division_df,x='DEPARTMENT_NAME')

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


# conn = init_connection()
    


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

