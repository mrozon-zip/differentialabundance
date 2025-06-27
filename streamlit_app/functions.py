import os
import fnmatch
import math
import pandas as pd
import streamlit as st

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def is_docker():
    return os.path.exists('/.dockerenv')


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