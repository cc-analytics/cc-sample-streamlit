import streamlit as st
import streamlit.components.v1 as components

# embed streamlit docs in a streamlit app
st.title("Online Sales in D3")
st.markdown(" Created with D3 and hosted on my Google Cloud")
components.iframe("https://tinyurl.com/4zv2fhc6", width = 1000, height = 800, scrolling = True)