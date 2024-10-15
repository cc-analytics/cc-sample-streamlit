import streamlit as st
from streamlit.components.v1 import html
from datetime import datetime
import pandas as pd
import altair as alt
from streamlit_pills import pills

# Utils imports
from utils import run_query, init_connection  

# Set Streamlit page configuration at the beginning
st.set_page_config(page_title="NYC Taxi A/B Test Demo", page_icon="🚕", layout="wide")

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
    st.title("🍎 NYC Taxi A/B Test Demo 🚕")
    # Sidebar
    st.sidebar.markdown("##### Created by: Chris Chen\n## Seasoned Data Analytics Professional\nchrischen.analytics@gmail.com\nhttps://www.linkedin.com/in/chrischenanalytics")

    # Tabs
    tab_about, tab_main, tab_to_dos = st.tabs(["About", "Main", "To-do's"])

    with tab_main:
        topic = pills(
        "",
        [
            # "Summary",
            "Data",
            "Analysis"
            # "Demographics",
            # "Dataframe"
        ],
        [
            # "📈",
            "📊",
            "💼"
            # "🧑",
            # "📃"
        ]
        # label_visibility="collapsed"
        )
        # df = load_people_data()
        if topic == "Summary":
            # show_trend(df)
            st.write("")
        elif topic == "Data":
            show_data()
        elif topic == "Analysis":
            show_analysis()
        # elif topic == "Demographics":
        #     show_demographics(df)
        # elif topic == "Dataframe":
        #     show_dataframe(df)

    with tab_about:
        st.write("""In this demo, I will showcase a statistical analysis by applying descriptive statistics and hypothesis testing to conduct a simulated **A/B test**. The focus of the analysis is to explore the relationship between fare amounts and payment types using the New York City Taxi & Limousine Commission (TLC) dataset. The answer we are trying to answer is:  """)
        st.write("""Do the customers who use a :orange[**credit card**] pay :orange[**higher fare**] amounts than those who use :orange[**cash**?]  """)
        st.write("")
        st.subheader(" What is an A/B Test?")
        st.markdown(
            """An A/B test is a statistical method used to compare two versions of something—such as a product, webpage, or process—to determine which performs better based on a specific metric. By randomly dividing participants into two groups (A and B), each group experiences a different version, and their responses are analyzed. This helps to identify significant differences between the two versions, allowing informed decisions based on data rather than assumptions. A/B testing is commonly used in marketing, user experience design, and product development.
    """
        )

    with tab_to_dos:
        with st.expander("To-do", expanded=True):
            st.write(
                """
            - Create a Tableau visualization
            - Deploy the chart component
            """
            )
            st.write("")
        with st.expander("Done", expanded=True):
            st.write(
                """
            - Set up app layout.
            - Show Python code.

            """
            )

def show_summary():
    summary_layout()

def show_data():
    data_layout()

def show_analysis():
    analysis_layout()
    
def show_demographics(df):
    demographics_layout(df)

def show_dataframe(df):
    dataframe_layout(df)    

# Layout
def summary_layout():
    "Summary"
    # col1, col2 = st.columns(2)
    # with col1:
    #     df['HIRED_DATE'] = pd.to_datetime(df['HIRED_DATE'])
    #     df['END_DATE'] = pd.to_datetime(df['END_DATE'])

    #     # # Generate date range
    #     date_range = pd.date_range(start=df['HIRED_DATE'].min(), end=datetime(2024,3,1))
    #     # # Initialize a Series to hold the count for each date
    #     date_counts = pd.Series(index=date_range, data='DATE')
    # # Count qualifying records for each date
    
    #     for single_date in date_range:
    #         date_counts[single_date] = ((df['HIRED_DATE'] <= single_date) &( (df['END_DATE'] >= single_date) | pd.isna(df['END_DATE']))).sum()
    #     label = "### Headcount Over Time: " + f"{date_counts.iloc[-1]:,}"
    #     st.markdown(label)        
    #     show_cumulative_headcount(date_counts)
    # with col2:
        # st.markdown("### Headcount by Division")
        # show_headcount_by_division(df)
        
def data_layout():
    # str = '<table><thead><tr><th ><p><span><strong><span>Column name</span></strong></span></p></th><th><p><span><strong><span>Description</span></strong></span></p></th></tr></thead><tbody><tr><td><p data-text-variant="body1"><span><span>ID</span></span></p></td><td><p data-text-variant="body1"><span><span>Trip identification number</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>VendorID</span></span></p></td><td><p data-text-variant="body1"><span><span>A code indicating the TPEP provider that provided the record.&nbsp; </span></span></p><p data-text-variant="body1"><span><strong><span>1= Creative Mobile Technologies, LLC; </span></strong></span></p><p data-text-variant="body1"><span><strong><span>2= VeriFone Inc.</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>tpep_pickup_datetime&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The date and time when the meter was engaged.&nbsp;</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>tpep_dropoff_datetime&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The date and time when the meter was disengaged.&nbsp;</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Passenger_count&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The number of passengers in the vehicle.&nbsp;&nbsp;</span></span></p><p data-text-variant="body1"><span><span>This is a driver-entered value.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Trip_distance&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The elapsed trip distance in miles reported by the taximeter.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>PULocationID&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>TLC Taxi Zone in which the taximeter was engaged</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>DOLocationID&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>TLC Taxi Zone in which the taximeter was disengaged</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>RateCodeID&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The final rate code in effect at the end of the trip.&nbsp;</span></span></p><p data-text-variant="body1"><span><strong><span>1= Standard rate&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>2=JFK&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>3=Newark&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>4=Nassau or Westchester&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>5=Negotiated fare&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>6=Group ride</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Store_and_fwd_flag&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>This flag indicates whether the trip record was held in vehicle memory before being sent to the vendor, aka “store and forward,”&nbsp; because the vehicle did not have a connection to the server.&nbsp;</span></span></p><p data-text-variant="body1"><span><strong><span>Y= store and forward trip&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>N= not a store and forward trip</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Payment_type&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>A numeric code signifying how the passenger paid for the trip.&nbsp; </span></span></p><p data-text-variant="body1"><span><strong><span>1= Credit card&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>2= Cash&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>3= No charge&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>4= Dispute&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>5= Unknown&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>6= Voided trip</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Fare_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The time-and-distance fare calculated by the meter.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Extra&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>MTA_tax&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>$0.50 MTA tax that is automatically triggered based on the metered rate in use.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Improvement_surcharge&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>$0.30 improvement surcharge assessed trips at the flag drop. The&nbsp; improvement surcharge began being levied in 2015.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Tip_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Tolls_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>Total amount of all tolls paid in trip.&nbsp;</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Total_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The total amount charged to passengers. Does not include cash tips.</span></span></p></td></tr></tbody></table>'
    # html(str, scrolling=True)
    st.subheader("Data dictionary")
    data = {
        'Columns': ["ID"
                    ,"VendorID"
                    ,"tpep_pickup_datetime"
                    ,"tpep_dropoff_datetime"
                    ,"Passenger_count"
                    ,"Trip_distance"
                    ,"PULocationID"
                    ,"DOLocationID"
                    ,"RateCodeID"
                    ,"Store_and_fwd_flag"
                    ,"Payment_type"
                    ,"Fare_amount"
                    ,"Extra"
                    ,"MTA_tax"
                    ,"Improvement_surcharge"
                    ,"Tip_amount"
                    ,"Tolls_amount"
                    ,"Total_amount"
                    ],
        'Description': ["Trip identification number."
                        ,"A code indicating the TPEP provider that provided the record.  1= Creative Mobile Technologies, LLC; \n 2= VeriFone Inc."
                        , "The date and time when the meter was engaged."
                        ,"The date and time when the meter was disengaged."
                        ,"The number of passengers in the vehicle.  This is a driver-entered value."
                        ,"The elapsed trip distance in miles reported by the taximeter."
                        ,"TLC Taxi Zone in which the taximeter was engaged"
                        ,"TLC Taxi Zone in which the taximeter was disengaged"
                        ,"The final rate code in effect at the end of the trip.  1= Standard rate  2=JFK  3=Newark  4=Nassau or Westchester  5=Negotiated fare  6=Group ride"
                        ,"This flag indicates whether the trip record was held in vehicle memory before being sent to the vendor, aka \"store and forward,\" because the vehicle did not have a connection to the server. Y= store and forward trip N= not a store and forward trip"
                        ,"A numeric code signifying how the passenger paid for the trip.  1= Credit card  2= Cash  3= No charge  4= Dispute  5= Unknown  6= Voided trip"
                        ,"The time-and-distance fare calculated by the meter."
                        ,"Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges."
                        ,"$0.50 MTA tax that is automatically triggered based on the metered rate in use."
                        ,"$0.30 improvement surcharge assessed trips at the flag drop. The  improvement surcharge began being levied in 2015."
                        ,"Tip amount - This field is automatically populated for credit card tips. Cash tips are not included."
                        ,"Total amount of all tolls paid in trip. "
                        ,"The total amount charged to passengers. Does not include cash tips."
]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)   
        
def analysis_layout():
    st.subheader("The experiment")
    st.write("The sample data comes from an experiment in which customers are randomly selected and divided into two groups: 1. customers who are required to pay with credit card, 2. customers who are required to pay with cash.")
    st.subheader("Goal")
    st.write("Apply descriptive statistics and hypothesis testing in Python to conduct an A/B test. My goal is to analyze whether there is a relationship between payment type and fare amount. For example, I will explore whether customers who use credit cards tend to pay higher fares compared to those who use cash.")
    body = '''import pandas as pd \nfrom scipy import stats as st\n# Load dataset into dataframe \ntaxi_data = pd.read_csv(\"2017_Yellow_Taxi_Trip_Data.csv\", index_col = 0)\n# Explore the data
taxi_data.groupby("payment_type")["fare_amount"].mean()    
# payment_type
# 1    13.429748
# 2    12.213546
# 3    12.186116
# 4     9.913043 \n
# 1 is credit card and 2 is cash.  Average fare amount is higher for credit card payment type.
    '''
    st.code(body, language="python")
    st.write("Based on the averages, it seems that customers who pay with credit cards tend to pay higher fares than those who use cash. However, this difference could simply be due to :orange[**random variation in the sample**] , rather than a genuine difference in fare amounts. To determine if the difference is statistically significant, you perform a :orange[hypothesis test].")
    st.subheader("Hypothesis testing")
    st.write("")
    st.latex("\Eta_0 : \t{\small There\ is\ NO\ difference\ in\ the\ average\ fare\ amount\ between\ customers\ who\ use\ credit\ cards\ and\ customers\ who\ use\ cash.}\\newline\Eta_a : \t{\small There\ IS\ a\ difference\ in\ the\ average\ fare\ amount\ between\ customers\ who\ use\ credit\ cards\ and\ customers\ who\ use\ cash.}")
    st.write('''Use 5% as the significance level and proceed with a two-sample t-test.''')
    st.latex("\\alpha = 0.005")
    st.write("Calculate p-value:")
    body2 = '''credit_payments = taxi_data[taxi_data["payment_type"]==1]["fare_amount"]
cash_payments = taxi_data[taxi_data["payment_type"]==2]["fare_amount"]
t_statistic, p_value = st.ttest_ind(credit_payments, cash_payments, equal_var=False)
print(f"T-statistic: {t_statistic}")
print(f"P-value: {p_value}")
# T-statistic: 6.866800855655372
# P-value: 6.797387473030518e-12
'''
    st.code(body2, language="python")
    st.write(":orange[**P-value is much smaller than 0.05, we reject the null hypothesis.**]  Since customers who are required to pay with credit cards tend to pay more, it should be encouraged.")
    st.write("This project operates under the assumption that passengers were required to use a specific payment method and consistently complied once informed. However, the data wasn't collected with this in mind, so random grouping was necessary to perform the A/B test. The dataset doesn't consider other plausible factors. For instance, riders may prefer credit cards for longer trips because they might not carry enough cash. In other words, it’s more likely that the fare amount influences the payment type, rather than the payment type determining the fare.")
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown("### Historical Hirings")
    #     show_hirings(df)
    # with col2:
    #     st.markdown("### Historical Departure")
    #     show_departures(df)

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
