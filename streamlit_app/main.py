import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

# Define the pages
main_page = st.Page("pages/main_page.py", title="Main Page")
page_2 = st.Page("pages/page2.py", title="GSEA Section")
page_3 = st.Page("pages/page3.py", title="DEseq2 Section")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

pg.run()