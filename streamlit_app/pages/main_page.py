import streamlit as st
import os
import json

folder_path='.'
full_folder_path = os.path.abspath(folder_path)

# Main page content
st.sidebar.markdown("# Main page")
st.title('Streamlit App for Differential Abundance Analysis')
st.markdown('This app is designed to visualize the results of differential abundance analysis and GSEA.')
st.markdown(f"**Please, input your output from differential abundance pipeline into** `{full_folder_path}`")

filenames = os.listdir(folder_path)
selected_filename = st.selectbox('Select a file', filenames)
#filename = os.path.join(folder_path, selected_filename)

st.write('You selected `%s`' % selected_filename)

with open("shared_config.json", "w") as f:
    json.dump({"filepath": f"{selected_filename}/"}, f)