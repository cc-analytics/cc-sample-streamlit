import streamlit as st
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
st.title("Retention example in D3")
st.markdown(" Created with D3 and hosted on my Google Cloud")
components.iframe("https://tinyurl.com/48kwcs4r", width = 1200, height = 760, scrolling = True)
st.sidebar.title("Chris Chen")
st.sidebar.markdown("# Seasoned Data Analytics Professional")
st.sidebar.markdown("chrischen.analytics@gmail.com")
st.sidebar.markdown("https://www.linkedin.com/in/chrischenanalytics")