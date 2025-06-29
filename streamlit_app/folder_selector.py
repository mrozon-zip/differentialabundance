import tkinter as tk
from tkinter import filedialog
import sys
import json
import streamlit as st

def select_folder():
    st.write("Please select a folder to continue.")
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()  # Open the dialog to select a folder
    if folder_path:
        print(json.dumps({"folder_path": folder_path}))
    root.destroy()

if __name__ == "__main__":
    select_folder()