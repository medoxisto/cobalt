import streamlit as st

st.title("Cobalt Media Downloader")

# Add your app interface here
url = st.text_input("Enter media URL")
if st.button("Download") and url:
    st.write(f"Processing download for: {url}")
    # Connect to your cobalt backend logic here
