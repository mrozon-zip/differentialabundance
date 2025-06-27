import pandas as pd
import streamlit as st
import plotly_express as px
from functions import find, is_docker, display_table_section

st.set_page_config(layout="wide")

# Define the pages
main_page = st.Page("main_page.py", title="Main Page")
page_2 = st.Page("page2.py", title="GSEA Section")
page_3 = st.Page("page3.py", title="DEseq2 Section")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

pg.run()

# Determine the source directory based on the environment
# If running locally, use the test directory; if in Docker, use the data directory
local = not is_docker()
docker = is_docker()

if local:
    source = '../differentialabundance/test/'
elif docker:
    source = 'data/'

gsea_files = find('*gsea_report_for_*.tsv', f"{source}report/gsea/")
tables_differential_files = find('*deseq2.results.tsv', f"{source}tables/differential/")
tables_annotation_files = find('**.tsv', f"{source}tables/annotation")

