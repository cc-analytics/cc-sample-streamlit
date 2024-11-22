import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt
import requests
from streamlit_pills import pills
from google.oauth2 import service_account
from google.cloud import bigquery
from folium.plugins import HeatMap
import folium
from streamlit_folium import st_folium

# Utils imports
from utils import run_query, init_connection  

# Set Streamlit page configuration at the beginning
st.set_page_config(page_title="Waymo Trip Data on Google Cloud", page_icon="🚗", layout="wide")

def main():
    st.title("Waymo Trip Data on Google Cloud 🚗")
    # Sidebar
    st.sidebar.markdown("##### Created by: Chris Chen\n## Seasoned Data Analytics Professional\nchrischen.analytics@gmail.com\nhttps://www.linkedin.com/in/chrischenanalytics")

    # Tabs
    # tab_about, tab_main, tab_to_dos = st.tabs(["About"])
    tab_about, tab_generate_data, tab_report = st.tabs(["About","AI Generate Data", "Report"])

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

    with tab_report:
        show_report()

def show_form():
    form_layout()

def show_data_definition():
    data_definition_layout()

def show_report():
    report_layout()

# Layout

def form_layout():
    with st.form("my_form"):

        st.write("Trip data gets AI generated and inserted into Google :orange[**BigQuery**] for analysis.")

        col1, col2, col3 = st.columns(3, gap="small")

        with col1:
            trip_count = st.number_input("Number of Trips", value=1, min_value=1, max_value=10, help="The maximum number of trip to generate is 2 per request.")

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

def report_layout():
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    # Initialize BigQuery client
    client = bigquery.Client(credentials=credentials)
    # Define your table ID
    table_id = "waymo-sandbox.waymo_mockup.trip_data"

    # Query the BigQuery table
    query = f"SELECT * FROM `{table_id}` order by insert_timestamp desc"

    # Perform query.
    # Uses st.cache_data to only rerun when the query changes or after 5 min.
    # st.write("Uses st.cache_data to only rerun when the query changes or after 5 min.")
    @st.cache_data(ttl=300)
    def run_query(query):
        query_job = client.query(query)
        rows_raw = query_job.result()
        # Convert to list of dicts. Required for st.cache_data to hash the return value.
        rows = [dict(row) for row in rows_raw]
        return rows
    
    # Load the query result into a Pandas DataFrame
    # df = client.query(query).to_dataframe()
    df = pd.DataFrame(run_query(query))

    clist = df[["start_latitude", "start_longitude"]].values.tolist()
    # San Francisco base map
    st.write("Heat map of the trip starting locations.")
    col1, col2 = st.columns([3,1])

    with col1:
        m = folium.Map([37.76, -122.41], zoom_start=12)
        HeatMap(clist).add_to(m)   
        st_data = st_folium(m, width=800, height = 480)
        st.write("Data:")    
        st.dataframe(df)

    with col2:
        st.date_input(label="Start Date")
        st.date_input(label="End Date")
        st.write("The filters are being implemented...")

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

if __name__ == "__main__":
    main()
