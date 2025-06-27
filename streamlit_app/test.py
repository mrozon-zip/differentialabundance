import math
import os, fnmatch
import pandas as pd
import streamlit as st
import plotly_express as px

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def is_docker():
    return os.path.exists('/.dockerenv')

st.set_page_config(layout="wide")
st.title('Streamlit App for Differential Abundance Analysis')
st.markdown('This app is designed to visualize the results of differential abundance analysis and GSEA.')

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

def display_table_section(title, files):
    st.header(title)
    if not files:
        st.warning(f"No {title} files found.")
        return

    tabs = st.tabs([os.path.basename(f) for f in files])
    for tab, file in zip(tabs, files):
        with tab:
            df = pd.read_csv(file, sep='\t')
            total_rows = len(df)
            entries_per_page = st.selectbox("Entries per page", [10, 20, 50, 100], index=0, key=f"{title}_{file}_entries_per_page")
            total_pages = math.ceil(total_rows / entries_per_page)

            page = st.number_input("Page", min_value=1, max_value=total_pages, step=1, key=f"{title}_{file}_page")
            start_idx = (page - 1) * entries_per_page
            end_idx = min(start_idx + entries_per_page, total_rows)

            st.dataframe(df.iloc[start_idx:end_idx])

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["GSEA", "Differential Abundance", "Annotation"])

if page == "GSEA":
    st.header("GSEA Section")
    display_table_section("GSEA", gsea_files)

elif page == "Differential Abundance":
    st.header("Differential Abundance Section")
    display_table_section("Differential", tables_differential_files)

elif page == "Annotation":
    st.header("Annotation Section")
    display_table_section("Annotation", tables_annotation_files)