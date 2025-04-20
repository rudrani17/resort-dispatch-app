import streamlit as st
import pandas as pd
from datetime import date
import os

# File path to save data
DATA_FILE = "dispatch_data.csv"

# Page Title
st.title("🌿 Nature's Sprouts Dispatch Organizer 🌱")
st.write("Welcome, my little worker bees!🐝✨ Come on, Let's organize those dispatches like a pro!")

# Function to load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Resort", "Material", "Quantity", "Dispatch Date", "Status", "Updated By"])

# Function to save new entry
def save_data(entry):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# FORM
st.header("Fill the Dispatch Form 📦")

with st.form("dispatch_form"):
    resort = st.selectbox("Resort Name 🏨", [
        "Village Machan, MP Pench", 
        "Kulamama, MP Pench", 
        "Tadoba Safari Stay, Moharli", 
        "Zeal Resort, Kolara", 
        "Singh Estate Resort, Zari", 
        "Gourissa, Madhai Satpura", 
        "Wildmark Resort, Kanha"
    ])
    material = st.text_input("📦 Material Name")
    quantity = st.number_input("🔢 Quantity", min_value=1)
    dispatch_date = st.date_input("🗓 Dispatch Date", value=date.today())
    status = st.selectbox("📍 Status", ["Pending", "In Transit", "Delivered"])
    worker_name = st.text_input("🧑‍🔧 Your Name")

    submitted = st.form_submit_button("Submit Dispatch ✅")

    if submitted:
        new_entry = {
            "Resort": resort,
            "Material": material,
            "Quantity": quantity,
            "Dispatch Date": dispatch_date.strftime("%d-%m-%Y"),
            "Status": status,
            "Updated By": worker_name
        }
        save_data(new_entry)
        st.success("Dispatch Info Submitted and Saved to File!")

# SHOW TABLE
st.header("📊 Dispatch Dashboard")

df = load_data()
if not df.empty:
    st.dataframe(df)
else:
    st.info("No dispatch data yet! Fill the form above to get started 🚚")

import io

# 📥 DOWNLOAD SECTION
st.header("📤 Export Dispatch Data")

if not df.empty:
    towrite = io.BytesIO()
    downloaded_file = df.to_excel(towrite, index=False, sheet_name='Dispatches')
    towrite.seek(0)

    st.download_button(
        label="📥 Download Excel File",
        data=towrite,
        file_name='dispatch_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.info("No data to export yet!")

