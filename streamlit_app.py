# streamlit_app.py
import streamlit as st
import subprocess
import os
import sys
import json
from pathlib import Path
import tempfile

st.set_page_config(
    page_title="Cobalt Media Downloader",
    page_icon="🔷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700;
        background: linear-gradient(90deg, #3494E6, #EC6EAD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #3494E6;
    }
    .formats-container {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        font-size: 0.8rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# Add header
st.markdown("<h1 class='main-header'>Cobalt Media Downloader</h1>", unsafe_allow_html=True)

# Function to run cobalt command
def run_cobalt(url, format=None, output_dir=None):
    try:
        base_command = ["python", "-m", "cobalt.cli.main"]
        
        # Add the URL
        base_command.extend(["--url", url])
        
        # Add format if specified
        if format and format != "Best quality (automatic)":
            base_command.extend(["--format", format])
            
        # Add output directory if specified
        if output_dir:
            base_command.extend(["--output", output_dir])
            
        # Add info flag to get available formats
        if "info" in locals() and info:
            base_command.append("--info")
            
        # Run command and capture output
        result = subprocess.run(
            base_command,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        return False, str(e)

# Function to fetch available formats
def get_formats(url):
    try:
        info_command = ["python", "-m", "cobalt.cli.main", "--url", url, "--info", "--json"]
        result = subprocess.run(
            info_command,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return None
            
        try:
            data = json.loads(result.stdout)
            formats = data.get("formats", [])
            return formats
        except json.JSONDecodeError:
            return None
    except Exception:
        return None

# Main app interface
url = st.text_input("Enter media URL", placeholder="https://example.com/video")

show_advanced = st.checkbox("Show advanced options")

if show_advanced:
    with st.expander("Advanced Options", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            download_dir = st.text_input("Download directory", value="downloads")
        
        with col2:
            if url:
                formats = get_formats(url)
                if formats:
                    format_options = ["Best quality (automatic)"] + [f"{f['format_id']} - {f['quality']} - {f['ext']}" for f in formats]
                    selected_format = st.selectbox("Format", format_options)
                    if selected_format != "Best quality (automatic)":
                        selected_format = selected_format.split(" - ")[0]
                else:
                    st.info("Enter a URL and click 'Check formats' to see available formats")
                    selected_format = "Best quality (automatic)"
            else:
                st.info("Enter a URL to see available formats")
                selected_format = "Best quality (automatic)"

# Create download button
if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            if show_advanced:
                success, output = run_cobalt(url, selected_format, download_dir)
            else:
                success, output = run_cobalt(url)
                
            if success:
                st.success("Download completed successfully!")
                st.code(output)
            else:
                st.error("Download failed")
                st.code(output)
    else:
        st.warning("Please enter a URL")

# Information section
with st.expander("About Cobalt"):
    st.markdown("""
    **Cobalt** is a media downloader that doesn't piss you off. It's friendly, efficient, and doesn't have ads, trackers, paywalls, or other nonsense.
    
    - Downloads videos and audio from various platforms
    - Simple and straightforward interface
    - No ads or trackers
    - Open source project
    
    Check out the [GitHub repository](https://github.com/medoxisto/cobalt) for more information.
    """)

# Footer
st.markdown("<div class='footer'>Cobalt Media Downloader • Open Source Project</div>", unsafe_allow_html=True)
