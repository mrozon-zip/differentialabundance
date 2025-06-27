import pandas as pd
import plotly.express as px
import os
import streamlit as st
from functions import find, is_docker, display_table_section



st.markdown("# DEseq2 Section")
st.sidebar.markdown("# DEsq2 Section")

local = not is_docker()
docker = is_docker()

if local:
    source = '../differentialabundance/test/'
elif docker:
    source = 'data/'

tables_differential_files = find('*deseq2.results.tsv', f"{source}tables/differential/")
tables_annotation_files = find('**.tsv', f"{source}tables/annotation")

# Merge all differential abundance tables into one DataFrame
merged_df = pd.concat(
    [pd.read_csv(f, sep='\t') for f in tables_differential_files if os.path.isfile(f)],
    ignore_index=True
)
# Round all numerical columns to 8 decimals
merged_df = merged_df.apply(lambda col: col.round(8) if pd.api.types.is_numeric_dtype(col) else col)

# Load annotation tables and merge them into one DataFrame
annotation_df = pd.concat(
    [pd.read_csv(f, sep='\t') for f in tables_annotation_files if os.path.isfile(f)],
    ignore_index=True
)

# Drop duplicates to ensure each gene_id maps to one gene_name
annotation_df = annotation_df[['gene_id', 'gene_name']].drop_duplicates()

# Merge annotation with differential abundance data on gene_id
if 'gene_id' in merged_df.columns and 'gene_id' in annotation_df.columns:
    merged_df = merged_df.merge(annotation_df, on='gene_id', how='left')

    # Create plots for each file
    plot_labels = ['Treated vs Control', 'KO vs WT']
    plot_dict = {}

    for label, file in zip(plot_labels, tables_differential_files):
        df = pd.read_csv(file, sep='\t')
        if 'gene_id' in df.columns and 'gene_id' in annotation_df.columns:
            df = df.merge(annotation_df, on='gene_id', how='left')
        df = df.apply(lambda col: col.round(8) if pd.api.types.is_numeric_dtype(col) else col)

        fig = px.scatter(
            df,
            x='log2FoldChange',
            y='padj',
            hover_data={'gene_name': True, 'log2FoldChange': False, 'padj': False},
            title=f'Differential Abundance: {label}'
        )
        x_max = max(abs(df['log2FoldChange'].min()), abs(df['log2FoldChange'].max()))
        fig.update_layout(xaxis_range=[-x_max, x_max])
        plot_dict[label] = fig

    # Select which plot to show
    selected_plot = st.selectbox("Select comparison to display:", plot_labels)
    st.plotly_chart(plot_dict[selected_plot])

    # Display tables in tabs with simplified labels
    tab_labels = [f"{i}" for i in plot_labels]
    num_tabs = min(len(tables_differential_files), len(tab_labels))
    tabs = st.tabs(tab_labels[:num_tabs])

    for tab, file in zip(tabs, tables_differential_files):
        with tab:
            st.write(f"**File:** {file}")
            df = pd.read_csv(file, sep='\t')

            entries_per_page = st.selectbox("Entries per page", [10, 25, 50, 100], key=f"entries_{file}")
            total_pages = (len(df) - 1) // entries_per_page + 1
            page = st.selectbox("Page", list(range(1, total_pages + 1)), key=f"page_{file}")

            start = (page - 1) * entries_per_page
            end = start + entries_per_page
            st.dataframe(df.iloc[start:end])