import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt
from streamlit_pills import pills

# Utils imports
from utils import run_query, init_connection  

# Set Streamlit page configuration at the beginning
st.set_page_config(page_title="New York City Taxi Demo", page_icon="🚕", layout="wide")

# # Decorator for caching data loading function
# @st.cache_data
# def load_people_data():
#     # query = "SELECT A.EMPLOYEE_ID, A.NAME, A.BIRTH_DATE, A.\"Education\" as EDUCATION, A.HIRED_DATE, A.JOB_NAME, A.DEPARTMENT_NAME, B.\"Division\" as DIVISION_NAME from CCMOCKUP.PUBLIC.EMPLOYEE_TEST A join CCMOCKUP.PUBLIC.DEPARTMENT_TEST B on A.DEPARTMENT_NAME = B.\"Department\""
#     query = "SELECT A.EMPLOYEE_ID, A.NAME, A.BIRTH_DATE, A.\"Education\" as EDUCATION, A.HIRED_DATE, A.JOB_NAME, A.DEPARTMENT_NAME, B.\"Division\" as DIVISION_NAME, DATEADD(DAY, C.EMPLOYED_LENGTH, A.HIRED_DATE) as END_DATE, C.IS_INVOLUNTARY_TERMINATION from CCMOCKUP.PUBLIC.EMPLOYEE_TEST A join CCMOCKUP.PUBLIC.DEPARTMENT_TEST B on A.DEPARTMENT_NAME = B.\"Department\" left join CCMOCKUP.PUBLIC.EMPLOYED_LENGTH_TEST C on A.EMPLOYEE_ID = C.EMPLOYEE_ID"
#     return run_query(query)

# def calculate_age(birth_date):
#     today = datetime.now()
#     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
#     return age

def main():
    st.title("New York City Taxi Demo 🍎🚕")
    # Sidebar
    st.sidebar.markdown("##### Created by: Chris Chen\n## Seasoned Data Analytics Professional\nchrischen.analytics@gmail.com\nhttps://www.linkedin.com/in/chrischenanalytics")

    # Tabs
    tab_about, tab_main, tab_to_dos = st.tabs(["About", "Main", "To-do's"])

    with tab_main:
        topic = pills(
        "",
        [
            "Trend",
            "Headcount",
            "Recruitment",
            "Demographics",
            "Dataframe"
        ],
        [
            "📈",
            "📊",
            "💼",
            "🧑",
            "📃"
        ]
        # label_visibility="collapsed"
        )
        # df = load_people_data()
        # if topic == "Trend":
        #     show_trend(df)
        # elif topic == "Headcount":
        #     show_headcount(df)
        # elif topic == "Recruitment":
        #     show_recruitment(df)
        # elif topic == "Demographics":
        #     show_demographics(df)
        # elif topic == "Dataframe":
        #     show_dataframe(df)

    with tab_about:
        st.write("""In this demo, I will showcase a statistical analysis by applying descriptive statistics and hypothesis testing to conduct an A/B test. The focus of the analysis is to explore the relationship between fare amounts and payment types using the New York City Taxi & Limousine Commission (TLC) dataset. The answer we are trying to answer is, do the customers who use a credit card pay higher fare amounts than those who use cash?  """)
        st.write("")
        st.subheader(" What is an A/B Test?")
        st.markdown(
            """An A/B test is a statistical method used to compare two versions of something—such as a product, webpage, or process—to determine which performs better based on a specific metric. By randomly dividing participants into two groups (A and B), each group experiences a different version, and their responses are analyzed. This helps to identify significant differences between the two versions, allowing informed decisions based on data rather than assumptions. A/B testing is commonly used in marketing, user experience design, and product development.
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

    with tab_to_dos:
        with st.expander("To-do", expanded=True):
            st.write(
                """
            - Create a Tableau visualization
            - Deploy the chart component
            - Include information in the 'Info' tab.
            """
            )
            st.write("")
        with st.expander("Done", expanded=True):
            st.write(
                """
            - Set up app layout.
         

            """
            )

def show_trend(df):
    trend_layout(df)

def show_headcount(df):
    headcount_layout(df)

def show_recruitment(df):
    recruitment_layout(df)
    
def show_demographics(df):
    demographics_layout(df)

def show_dataframe(df):
    dataframe_layout(df)    

# Layout
def trend_layout(df):
    col1, col2 = st.columns(2)
    with col1:
        df['HIRED_DATE'] = pd.to_datetime(df['HIRED_DATE'])
        df['END_DATE'] = pd.to_datetime(df['END_DATE'])

        # # Generate date range
        date_range = pd.date_range(start=df['HIRED_DATE'].min(), end=datetime(2024,3,1))
        # # Initialize a Series to hold the count for each date
        date_counts = pd.Series(index=date_range, data='DATE')
    # Count qualifying records for each date
    
        for single_date in date_range:
            date_counts[single_date] = ((df['HIRED_DATE'] <= single_date) &( (df['END_DATE'] >= single_date) | pd.isna(df['END_DATE']))).sum()
        label = "### Headcount Over Time: " + f"{date_counts.iloc[-1]:,}"
        st.markdown(label)        
        show_cumulative_headcount(date_counts)
    # with col2:
        # st.markdown("### Headcount by Division")
        # show_headcount_by_division(df)
        
def headcount_layout(df):
    r1col1, r1col2 = st.columns(2)
    with r1col1:
        st.markdown("### Headcount by Division")
        show_headcount_by_division(df)
    with r1col2:
        st.markdown("### Headcount by Department")
        show_headcount_by_department(df)        
        
def recruitment_layout(df):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Historical Hirings")
        show_hirings(df)
    with col2:
        st.markdown("### Historical Departure")
        show_departures(df)

def demographics_layout(df):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Headcount by Age")
        show_headcount_by_age(df)
    with col2:
        st.markdown("### Headcount by Education")
        show_headcount_by_education(df)

def dataframe_layout(df):
    col1, col2 = st.columns(2)
    with col1:
        show_dataframe(df)    

# Actual implementation
def show_cumulative_headcount(df):
     chart = st.line_chart(df, width=200, height=260)

def show_headcount_by_division(df):
    counts_by_division_df = df.groupby('DIVISION_NAME')['DIVISION_NAME'].count().reset_index(name='Count')
    bar_chart = st.bar_chart(data=counts_by_division_df,x='DIVISION_NAME')

def show_headcount_by_department(df):
    counts_by_department_df = df.groupby('DEPARTMENT_NAME')['DEPARTMENT_NAME'].count().reset_index(name='Count')
    bar_chart = st.bar_chart(data=counts_by_department_df,x='DEPARTMENT_NAME')

def show_headcount_by_age(df):
    df['AGE'] = df['BIRTH_DATE'].apply(calculate_age)
    counts_by_age_df = df.groupby('AGE')['AGE'].count().reset_index(name='Count')
    bar_chart = st.bar_chart(data=counts_by_age_df,x='AGE')

def show_headcount_by_education(df):
    counts_by_education_df = df.groupby('EDUCATION')['EDUCATION'].count().reset_index(name='Count')
    bar_chart = st.bar_chart(data=counts_by_education_df,x='EDUCATION')   

def show_hirings(df):
    hiring_counts_df = df.groupby('HIRED_DATE')['HIRED_DATE'].count().reset_index(name='Count')    
    # chart = st.line_chart(hiring_counts_df.set_index('HIRED_DATE'),width=200, height=260)
    chart = st.line_chart(hiring_counts_df, x="HIRED_DATE", y="Count", width=200, height=260)

def show_departures(df):
    df['END_DATE'] = pd.to_datetime(df['END_DATE'])
    df = df[df['END_DATE'] < datetime.today()]
    departures_counts_df = df.groupby('END_DATE')['END_DATE'].count().reset_index(name='Count')    
    chart = st.line_chart(departures_counts_df, x="END_DATE", y="Count", width=200, height=260)    

def show_dataframe(df):
    st.markdown("###### Dataframe created from Snowflake Database")
    st.dataframe(df)   

if __name__ == "__main__":
    main()