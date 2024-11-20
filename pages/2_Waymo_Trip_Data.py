import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt
import requests
from streamlit_pills import pills

# Utils imports
from utils import run_query, init_connection  

# Set Streamlit page configuration at the beginning
st.set_page_config(page_title="Waymo Trip Data on Google Cloud", page_icon="🚗", layout="wide")

# Decorator for caching data loading function
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
    st.title("Waymo Trip Data on Google Cloud 🚗")
    # Sidebar
    st.sidebar.markdown("##### Created by: Chris Chen\n## Seasoned Data Analytics Professional\nchrischen.analytics@gmail.com\nhttps://www.linkedin.com/in/chrischenanalytics")

    # Tabs
    # tab_about, tab_main, tab_to_dos = st.tabs(["About"])
    tab_about, tab_generate_data = st.tabs(["About","AI Generate Data"])

    with tab_generate_data:
        topic = pills(
        "",
        [
            "AI Generate Data",
            "Data Definition"
        #     "Recruitment",
        #     "Demographics",
        #     "Dataframe"
        ],
        [
            "🚘",
            "📄"
        #     "💼",
        #     "🧑",
        #     "📃"
        ]
        # label_visibility="collapsed"
        )
        # df = load_people_data()
        if topic == "AI Generate Data":
            show_form()
        elif topic == "Data Definition":
            show_data_definition()
        # elif topic == "Recruitment":
        #     show_recruitment(df)
        # elif topic == "Demographics":
        #     show_demographics(df)
        # elif topic == "Dataframe":
        #     show_dataframe(df)

    with tab_about:
        st.write("While exploring a career opportunity at Waymo, I envisioned what their data ecosystem might look like and decided to create a demo to bring this idea to life. As a data professional, I leveraged my expertise to experiment with various cloud technologies. Currently, I am developing a self-serve BI application using :orange[**Google Cloud Platform**] to showcase my skills and understanding. ")
        st.write("")                 
        st.write("The data pipeline is designed to ingest and store data in :orange[**BigQuery**] for reporting and analysis. ")
        st.write("")  
        st.write("To simulate trip data, I use my :orange[**OpenAI API**] account to generate Waymo trips in San Francisco.  The generation pipeline is scheduled to run once every hour on :orange[**Cloud Run Function**]. Then the stream of data is ingested into a :orange[**BigQuery**] table partitioned by trip_date to enhance query performance. Finally, I leverage :orange[**Streamlit**]  to develop a self-service BI application for analyzing and visualizing the data.")
        st.write("")
        st.write("There are many ways to implement this, but I chose this particular design to keep things interesting while maintaining a low cost profile.  One thing I've learned from using cloud technologies is that while they are very convenient, your wallet can quickly get burned if you don't choose wisely. The rule of thumb is to use only what you need but keep it flexible and scalable. You can then quickly scale up if needed. ")

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

    # with tab_to_dos:
    #     with st.expander("To-do", expanded=True):
    #         st.write(
    #             """
    #         - Add more metrics
    #         """
    #         )
    #         st.write("")
    #     with st.expander("Done", expanded=True):
    #         st.write(
    #             """
    #         - Add a link to the Tableau version
    #         - Deploy the chart component
    #         - Include information in the 'Info' tab.
    #         - Set up app layout.
    #         - Create Snowflake tables.
    #         - Populate mock-up data gnerated by GPT-4.
    #         - Create People Analytics metrics.

    #         """
    #         )

def show_form():
    form_layout()

def show_data_definition():
    data_definition_layout()
# def show_headcount(df):
#     headcount_layout(df)

# def show_recruitment(df):
#     recruitment_layout(df)
    
# def show_demographics(df):
#     demographics_layout(df)

# def show_dataframe(df):
#     dataframe_layout(df)    

# # Layout
# def trend_layout(df):
#     col1, col2 = st.columns(2)
#     with col1:
#         df['HIRED_DATE'] = pd.to_datetime(df['HIRED_DATE'])
#         df['END_DATE'] = pd.to_datetime(df['END_DATE'])

#         # # Generate date range
#         date_range = pd.date_range(start=df['HIRED_DATE'].min(), end=datetime(2024,3,1))
#         # # Initialize a Series to hold the count for each date
#         date_counts = pd.Series(index=date_range, data='DATE')
#     # Count qualifying records for each date
    
#         for single_date in date_range:
#             date_counts[single_date] = ((df['HIRED_DATE'] <= single_date) &( (df['END_DATE'] >= single_date) | pd.isna(df['END_DATE']))).sum()
#         label = "### Headcount Over Time: " + f"{date_counts.iloc[-1]:,}"
#         st.markdown(label)        
#         show_cumulative_headcount(date_counts)
#     # with col2:
#         # st.markdown("### Headcount by Division")
#         # show_headcount_by_division(df)
        
# def headcount_layout(df):
#     r1col1, r1col2 = st.columns(2)
#     with r1col1:
#         st.markdown("### Headcount by Division")
#         show_headcount_by_division(df)
#     with r1col2:
#         st.markdown("### Headcount by Department")
#         show_headcount_by_department(df)        
        
# def recruitment_layout(df):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("### Historical Hirings")
#         show_hirings(df)
#     with col2:
#         st.markdown("### Historical Departure")
#         show_departures(df)

# def demographics_layout(df):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("### Headcount by Age")
#         show_headcount_by_age(df)
#     with col2:
#         st.markdown("### Headcount by Education")
#         show_headcount_by_education(df)

# def dataframe_layout(df):
#     col1, col2 = st.columns(2)
#     with col1:
#         show_dataframe(df)    
def form_layout():
    with st.form("my_form"):

        st.write("Trip data gets AI generated and inserted into Google :orange[**BigQuery**] for analysis.")

        col1, col2, col3 = st.columns(3, gap="small")

        with col1:
            trip_count = st.number_input("Number of Trips", value=1, min_value=1, max_value=2, help="The maximum number of trip to generate is 2 per request.")

        with col2:
            trip_date = st.date_input("Trip Date", help="Date of the generated trip.")


        # col1, col2 = st.columns(2, gap="medium")

        st.write("")
        
        # submitted = st.form_submit_button("Generate Trip Data! ✨")
        if st.form_submit_button("Generate Trip Data! ✨"):
            # Prepare the data payload
            payload = {
                "trip_count": trip_count,
                "trip_date": str(trip_date)
            }

            try:
                url = "https://us-west1-waymo-sandbox.cloudfunctions.net/gen-waymo-trip-data"
                # Send the POST request
                response = requests.post(url, json=payload)
                
                # Display the response
                if response.status_code == 200:
                    st.success("Request was successful!")
                    # st.json(response.json())  # Display JSON response
                else:
                    st.error(f"Request failed with status code {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

def data_definition_layout():
    # str = '<table><thead><tr><th ><p><span><strong><span>Column name</span></strong></span></p></th><th><p><span><strong><span>Description</span></strong></span></p></th></tr></thead><tbody><tr><td><p data-text-variant="body1"><span><span>ID</span></span></p></td><td><p data-text-variant="body1"><span><span>Trip identification number</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>VendorID</span></span></p></td><td><p data-text-variant="body1"><span><span>A code indicating the TPEP provider that provided the record.&nbsp; </span></span></p><p data-text-variant="body1"><span><strong><span>1= Creative Mobile Technologies, LLC; </span></strong></span></p><p data-text-variant="body1"><span><strong><span>2= VeriFone Inc.</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>tpep_pickup_datetime&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The date and time when the meter was engaged.&nbsp;</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>tpep_dropoff_datetime&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The date and time when the meter was disengaged.&nbsp;</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Passenger_count&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The number of passengers in the vehicle.&nbsp;&nbsp;</span></span></p><p data-text-variant="body1"><span><span>This is a driver-entered value.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Trip_distance&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The elapsed trip distance in miles reported by the taximeter.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>PULocationID&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>TLC Taxi Zone in which the taximeter was engaged</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>DOLocationID&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>TLC Taxi Zone in which the taximeter was disengaged</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>RateCodeID&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The final rate code in effect at the end of the trip.&nbsp;</span></span></p><p data-text-variant="body1"><span><strong><span>1= Standard rate&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>2=JFK&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>3=Newark&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>4=Nassau or Westchester&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>5=Negotiated fare&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>6=Group ride</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Store_and_fwd_flag&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>This flag indicates whether the trip record was held in vehicle memory before being sent to the vendor, aka “store and forward,”&nbsp; because the vehicle did not have a connection to the server.&nbsp;</span></span></p><p data-text-variant="body1"><span><strong><span>Y= store and forward trip&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>N= not a store and forward trip</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Payment_type&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>A numeric code signifying how the passenger paid for the trip.&nbsp; </span></span></p><p data-text-variant="body1"><span><strong><span>1= Credit card&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>2= Cash&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>3= No charge&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>4= Dispute&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>5= Unknown&nbsp;</span></strong></span></p><p data-text-variant="body1"><span><strong><span>6= Voided trip</span></strong></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Fare_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The time-and-distance fare calculated by the meter.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Extra&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>MTA_tax&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>$0.50 MTA tax that is automatically triggered based on the metered rate in use.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Improvement_surcharge&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>$0.30 improvement surcharge assessed trips at the flag drop. The&nbsp; improvement surcharge began being levied in 2015.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Tip_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Tolls_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>Total amount of all tolls paid in trip.&nbsp;</span></span></p></td></tr><tr><td><p data-text-variant="body1"><span><span>Total_amount&nbsp;</span></span></p></td><td><p data-text-variant="body1"><span><span>The total amount charged to passengers. Does not include cash tips.</span></span></p></td></tr></tbody></table>'
    # html(str, scrolling=True)
    st.subheader("Data dictionary")
    data = {
        'Columns': ["trip_id"
                    ,"trip_date"
                    ,"trip_datetime"
                    ,"vehicle_id"
                    ,"start_latitude"
                    ,"start_longitude"
                    ,"end_latitude"
                    ,"end_longitude"
                    ,"distance_miles"
                    ,"trip_duration"
                    ,"route_details"
                    ,"payment_amount"
                    ,"payment_method"
                    ,"insert_timestamp"
                    ],
        'Description': ["Unique identifier for each trip.  UUID format."
                        ,"Date of the trip start."
                        ,"Datetime of the trip start"
                        ,"ID of the Waymo vehicle"
                        ,"Start location latitude."
                        ,"Start location longitude."
                        ,"End location latitude."
                        ,"End location longitude."
                        ,"Total distance covered in the trip."
                        ,"List of stops or significant points (optional)"
                        ,"A numeric code signifying how the passenger paid for the trip.  1= Credit card  2= Cash  3= No charge  4= Dispute  5= Unknown  6= Voided trip"
                        ,"Amount billed for the trip."
                        ,"Payment type (e.g., credit card, in-app billing)."
                        ,"Data insert timestamp."
]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)   

# # Actual implementation

# def show_cumulative_headcount(df):
#      chart = st.line_chart(df, width=200, height=260)

# def show_headcount_by_division(df):
#     counts_by_division_df = df.groupby('DIVISION_NAME')['DIVISION_NAME'].count().reset_index(name='Count')
#     bar_chart = st.bar_chart(data=counts_by_division_df,x='DIVISION_NAME')

# def show_headcount_by_department(df):
#     counts_by_department_df = df.groupby('DEPARTMENT_NAME')['DEPARTMENT_NAME'].count().reset_index(name='Count')
#     bar_chart = st.bar_chart(data=counts_by_department_df,x='DEPARTMENT_NAME')

# def show_headcount_by_age(df):
#     df['AGE'] = df['BIRTH_DATE'].apply(calculate_age)
#     counts_by_age_df = df.groupby('AGE')['AGE'].count().reset_index(name='Count')
#     bar_chart = st.bar_chart(data=counts_by_age_df,x='AGE')

# def show_headcount_by_education(df):
#     counts_by_education_df = df.groupby('EDUCATION')['EDUCATION'].count().reset_index(name='Count')
#     bar_chart = st.bar_chart(data=counts_by_education_df,x='EDUCATION')   

# def show_hirings(df):
#     hiring_counts_df = df.groupby('HIRED_DATE')['HIRED_DATE'].count().reset_index(name='Count')    
#     # chart = st.line_chart(hiring_counts_df.set_index('HIRED_DATE'),width=200, height=260)
#     chart = st.line_chart(hiring_counts_df, x="HIRED_DATE", y="Count", width=200, height=260)

# def show_departures(df):
#     df['END_DATE'] = pd.to_datetime(df['END_DATE'])
#     df = df[df['END_DATE'] < datetime.today()]
#     departures_counts_df = df.groupby('END_DATE')['END_DATE'].count().reset_index(name='Count')    
#     chart = st.line_chart(departures_counts_df, x="END_DATE", y="Count", width=200, height=260)    

# def show_dataframe(df):
#     st.markdown("###### Dataframe created from Snowflake Database")
#     st.dataframe(df)   

if __name__ == "__main__":
    main()
