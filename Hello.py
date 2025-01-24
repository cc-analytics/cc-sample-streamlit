# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import folium
import streamlit as st
from streamlit.logger import get_logger
from streamlit_folium import st_folium

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    st.title("Welcome to My Sandbox")
    st.markdown("### A showcase of my journey and expertise in data analytics, BI, and cloud technologies.")
    row1 = st.columns(2, gap="medium")
    with row1[0]:
        st.write("As a passionate professional with over 12 years of experience in the data field, committed to the ever-evolving landscape of system design and programming, I've created this platform to share my experiences, projects, and insights gained outside of my regular job. On this website, you'll discover detailed examples of my work with various cloud technologies, showcasing how I tackle complex challenges and contribute to the advancement of data-driven decision-making from my personal projects. This site also serves as my personal learning ground, helping me stay at the forefront of technological innovation. ")
        st.write("Whether you're a fellow enthusiast, a potential collaborator, or someone curious about the power of data analytics and cloud computing, I invite you to explore my portfolio and share in the journey of continuous learning and improvement.")
    with row1[1]:        
        st.markdown("##### Restaurants I enjoy near Dublin, CA:  ")
        # Some restaurants I like around Dublin

        m = folium.Map(location=[37.70286733532977, -121.87460047508559], zoom_start=13)
        st.write("Yin Ji Chang Fen: Healthy & light Cantonese food.")
        st.write("Mayflower Restaurant: Good Dimsum.")
        st.write("Cafe Tazza: Authentic Indian food.")
        st.write("Sata Japanese Restaurant: Authentic Japanese sushi.")
        snow_icon = folium.map.Icon(color='lightblue')
        # folium.Marker(location=[37.70286733532977, -121.87460047508559], popup="Snowflake", icon=snow_icon
        # ).add_to(m)
        folium.Marker(
            [37.69562641280019, -121.85025333314333], popup="Yin Ji Chang Fen", tooltip="Healthy & light"
        ).add_to(m)
        folium.Marker(
            [37.70407465648592, -121.86595372989773], popup="Mayflower Restaurant", tooltip="Good Dimsum"
        ).add_to(m)
        folium.Marker(
            [37.70528970455323, -121.8816482744688], popup="Cafe Tazza", tooltip="Authentic Indian"
        ).add_to(m)
        folium.Marker(
            [37.677234124306, -121.89701156642151], popup="Sato Japanese Restaurant", tooltip="Authentic Japanese"
        ).add_to(m)
        # call to render Folium map in Streamlit
        st_data = st_folium(m, width=350, height = 400)
    st.write("Created with Streamlit")
    st.write("")
    st.sidebar.markdown("##### Created by:")
    st.sidebar.markdown("# Chris Chen")
    st.sidebar.markdown("## Seasoned Data Analytics Professional")
    st.sidebar.markdown("chrischen.analytics@gmail.com")
    st.sidebar.markdown("https://www.linkedin.com/in/chrischenanalytics")
    st.sidebar.success("Select a demo above.")
    
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
