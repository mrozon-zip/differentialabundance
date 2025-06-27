import streamlit as st
from functions import find, is_docker, display_table_section
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.markdown("# GSEA Section")
st.sidebar.markdown("# GSEA Section")

local = not is_docker()
docker = is_docker()

if local:
    source = '../differentialabundance/test/'
elif docker:
    source = 'data/'

gsea_files = find('*gsea_report_for_*.tsv', f"{source}report/gsea/")

# Let user select which graph to display
graph_options = [
    "Treated and Control (ES)",
    "KO and WT (ES)",
    "Treated and Control (NES)",
    "KO and WT (NES)"
]
selected_option = st.selectbox("Select GSEA plot to display:", graph_options)

if "NES" in selected_option:
    sort_options = ["p adjusted (FDR q-val)", "Normalized Enrichment Score", "Size"]
else:
    sort_options = ["p adjusted (FDR q-val)", "Enrichment Score", "Size"]
sort_by = st.selectbox("Sort y-axis by:", sort_options)

gsea_dfs = []
for file in gsea_files:
    df = pd.read_csv(file, sep='\t')
    gsea_dfs.append(df)

# Create a dictionary to map selections to data combinations
selection_map = {
    "Treated and Control (ES)": ([0, 1], "ES"),
    "KO and WT (ES)": ([2, 3], "ES"),
    "Treated and Control (NES)": ([0, 1], "NES"),
    "KO and WT (NES)": ([2, 3], "NES")
}

selected_indices, score_type = selection_map[selected_option]
selected_dfs = [gsea_dfs[i] for i in selected_indices if i < len(gsea_dfs)]

if selected_dfs:
    merged_df = pd.concat(selected_dfs, ignore_index=True)
    merged_df = merged_df[['NAME', score_type, 'SIZE', 'FDR q-val']].dropna()

    sort_column_map = {
    "p adjusted (FDR q-val)": "FDR q-val",
    "Enrichment Score": "ES",
    "Normalized Enrichment Score": "NES",
    "Size": "SIZE"
    } 

    sort_column = sort_column_map[sort_by]

    # Ensure sort_column exists in DataFrame
    if sort_column not in merged_df.columns and sort_column != score_type:
        merged_df[sort_column] = [None] * len(merged_df)

    if sort_column in merged_df.columns:
        merged_df = merged_df.sort_values(by=sort_column, ascending=False)

    merged_df['size_scaled'] = (merged_df['SIZE'] - merged_df['SIZE'].min()) / (merged_df['SIZE'].max() - merged_df['SIZE'].min()) * 200 + 50

    fig = px.scatter(
        merged_df,
        x=score_type,
        y='NAME',
        size='size_scaled',
        color='FDR q-val',
        color_continuous_scale='RdBu',
        hover_data={
            score_type: True,
            'size_scaled': True,
            'FDR q-val': True,
            'NAME': False
        },
        labels={
            score_type: f"{score_type} Score",
            'NAME': 'Gene Set Name',
            'FDR q-val': 'FDR q-val',
            'size_scaled': 'Size'
        },
        title=f'GSEA Dot Plot: {selected_option}',
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=max(600, len(merged_df) * 30),
        margin=dict(r=150)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No GSEA data available for selected option: {selected_option}")


# Display tables in tabs with simplified names
tab_labels = ["Treated", "Control", "WT", "KO"]
num_tabs = min(len(gsea_files), len(tab_labels))
tabs = st.tabs(tab_labels[:num_tabs])

for tab, file in zip(tabs, gsea_files):
    with tab:
        st.write(f"**File:** {file}")
        df = pd.read_csv(file, sep='\t')
        # Pagination controls
        entries_per_page = st.selectbox("Entries per page", [10, 25, 50, 100], key=f"entries_{file}")
        total_pages = (len(df) - 1) // entries_per_page + 1
        page = st.selectbox("Page", list(range(1, total_pages + 1)), key=f"page_{file}")

        start = (page - 1) * entries_per_page
        end = start + entries_per_page
        st.dataframe(df.iloc[start:end])
