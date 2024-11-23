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
from streamlit_folium import folium_static

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
    tab_about, tab_generate_data, tab_heatmap = st.tabs(["About","AI Generate Data", "Heat Map"])

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
        
        if topic == "AI Generate Data":
            show_form()
        elif topic == "Data Definition":
            show_data_definition()
        
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

    with tab_heatmap:
        show_heatmap()

def show_form():
    form_layout()

def show_data_definition():
    data_definition_layout()

def show_heatmap():
    heatmap_layout()

# Layout

def form_layout():
    with st.form("my_form"):

        st.write("Trip data gets AI generated and inserted into Google :orange[**BigQuery**] for analysis.")

        col1, col2, col3 = st.columns(3, gap="small")

        with col1:
            trip_count = st.number_input("Number of Trips", value=1, min_value=1, max_value=10, help="The maximum number of trip to generate is 10 per request.")
            prompt_hint = st.text_input("Trip location hint (Optional):", help="Enter hint of locations for the trips.")

        with col2:
            trip_date = st.date_input("Trip Date", help="Date of the generated trip.")


        # col1, col2 = st.columns(2, gap="medium")

        st.write("")
        
        # submitted = st.form_submit_button("Generate Trip Data! ✨")
        if st.form_submit_button("Generate Trip Data! ✨"):
            # Prepare the data payload
            payload = {
                "trip_count": trip_count,
                "trip_date": str(trip_date),
                "prompt_hint": prompt_hint
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

def heatmap_layout():
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    # Initialize BigQuery client
    client = bigquery.Client(credentials=credentials)
    # Define your table ID
    table_id = "waymo-sandbox.waymo_mockup.trip_data"

    # Query the BigQuery table
    query = f"SELECT * FROM `{table_id}` order by insert_timestamp desc limit 1000"

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
    df["trip_date"] = pd.to_datetime(df["trip_date"]) # Convert to datetime
    
    col1, col2 = st.columns([3,1])
    # Initialize session state for map visibility
    if "map_center" not in st.session_state:
        st.session_state.map_center = [37.76, -122.41]  # Default center
    if "map_zoom" not in st.session_state:
        st.session_state.map_zoom = 12  # Default zoom

    if "show_map" not in st.session_state:
        st.session_state.show_map = True

    with col2:
        start_date = st.date_input("Start Date",datetime.strptime("2024-05-01", '%Y-%m-%d').date() )
        end_date = st.date_input("End Date", datetime.today())
        payment_method = st.radio("Payment Method", ["Any", "credit card", "in-app billing"], index=0)
    
    filtered_df = df

    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = filtered_df[(filtered_df['trip_date'] >= start_date) & (filtered_df['trip_date'] <= end_date)]
    
    if payment_method in ["credit card", "in-app billing"]:
        filtered_df = filtered_df[filtered_df['payment_method'] == payment_method]

    clist = filtered_df[["start_latitude", "start_longitude"]].values.tolist()    
    

    with col1:
        st.write("Click the button to toggle :orange[**Heat map**] of the trip starting locations.")
        # Button to toggle map visibility
        if st.button("Toggle Heat Map"):
            st.session_state.show_map = not st.session_state.show_map
            # st.session_state.map_center = [37.76, -122.41]  # Default center
            # st.session_state.map_zoom = 12  # Default zoom
        if st.session_state.show_map:
            # San Francisco base map
            with st.container(height = 510):
                m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.map_zoom)
                HeatMap(clist).add_to(m)   
                # # Add a JavaScript listener to capture map zoom and center
                # capture_js = """
                # <script>
                #     function captureMapState(map) {
                #         map.on('zoomend', function() {
                #             const zoomLevel = map.getZoom();
                #             const center = map.getCenter();
                #             const state = JSON.stringify({ zoom: zoomLevel, center: center });
                #             document.getElementById('map_state').value = state;
                #             document.getElementById('map_state').dispatchEvent(new Event('change'));
                #         });
                #         map.on('moveend', function() {
                #             const zoomLevel = map.getZoom();
                #             const center = map.getCenter();
                #             const state = JSON.stringify({ zoom: zoomLevel, center: center });
                #             document.getElementById('map_state').value = state;
                #             document.getElementById('map_state').dispatchEvent(new Event('change'));
                #         });
                #     }
                #     setTimeout(() => {
                #         if (window.map) {
                #             captureMapState(window.map);
                #         }
                #     }, 500);
                # </script>
                # <input type="hidden" id="map_state" name="map_state" value="">
                # """
                # # Add the custom JavaScript to the map
                # m.get_root().html.add_child(folium.Element(capture_js))
                st_data = st_folium(m, width=800, height = 480)
            # st_data = folium_static(m, width=800, height 
                # st.session_state.map_zoom = st_data.get("zoom")
                # cdata = st_data.get("center")
                # if cdata:
                    # st.session_state.map_center = [cdata["lat"],cdata["lng"]] 
                # Update session state based on user interaction
                # if st_data:
                #     # st.write("Raw map_data:", st_data)
                #     cdata = st_data.get("center")
                #     if cdata:
                #         updated_center = [st_data["center"]["lat"], st_data["center"]["lng"]]
                #         if updated_center != st.session_state.map_center:
                #             st.session_state.map_center = updated_center
                #             # st.experimental_rerun() 
                #     zdata = st_data.get("zoom")
                #     if zdata:
                #         updated_zoom = st_data["zoom"]
                #         if (updated_zoom != st.session_state.map_zoom):
                #             st.session_state.map_zoom = updated_zoom
                            # st.experimental_rerun() 

                # # Display the captured map state
                # st.write("Map Center:", st.session_state.map_center)
                # st.write("Zoom Level:", st.session_state.map_zoom)

        st.write("Data: (query results cached with 5 minutes timeout)")
        if st.button("Force Refresh"):
            run_query.clear()  # Clear the cache for this function    
        st.dataframe(filtered_df)
    # with col2:
    #     zoom_level = st.text_input("Zoom level", value=st_data.get("zoom"))
        
    

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
