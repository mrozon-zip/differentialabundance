import streamlit as st
import os
import json
import streamlit as st
import subprocess
import json
import os

# Main page content
st.sidebar.markdown("# Main page")
st.title('Streamlit App for Differential Abundance Analysis')
st.markdown('This app is designed to visualize the results of differential abundance analysis and GSEA.')
st.markdown('Please select a folder that contains the output of the differential abundance pipeline.')

folder_selected = False

st.title("Folder Selection and Management")
if st.button("Select Folder"):
    result = subprocess.run(["python", "/Users/krzysztofmrozik/Desktop/coding_challange/nf_streamlit_small_app/streamlit_app/folder_selector.py"], capture_output=True, text=True)
    st.write(result)  # Display the output from the folder selector script
    if result.returncode == 0:
        folder_data = json.loads(result.stdout)
        folder_path = folder_data.get("folder_path")
        if folder_path:
            st.success(f"Selected Folder: {folder_path}")
            required_folders = ['report', 'tables', 'process']
            missing_folders = [folder for folder in required_folders if not os.path.exists(os.path.join(folder_path, folder))]
            if not missing_folders:
                st.write("That is a correct output folder")
            else:
                st.write("Make sure that you select folder that was produced by differential abundance pipeline.")
            # List files and folders in the selected folder as an example
            items = os.listdir(folder_path)
            folder_selected = True
        else:
            st.error("No folder selected")
    else:
        st.error("Error selecting folder")


if folder_selected :
    st.write('You selected `%s`' % folder_path)

    st.write("Once you select a correct folder, you can see the results for GSEA and DEseq2 by clicking corresponding page in the sidebar.")

    with open("shared_config.json", "w") as f:
        json.dump({"filepath": f"{folder_path}/"}, f)