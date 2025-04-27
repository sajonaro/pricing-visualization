import streamlit as st
import json

# Load pricing data from JSON file
try:
    with open('data.json', 'r') as f:
        pricing_data = json.load(f)
except FileNotFoundError:
    st.error("Error: data.json not found. Make sure the file is in the same directory as the script.")
    st.stop()
except json.JSONDecodeError:
    st.error("Error: Invalid JSON format in data.json.")
    st.stop()

azure_data = pricing_data.get('app_containers')
gke_data = pricing_data.get('gke')

if not azure_data or not gke_data:
    st.error("Error: 'app_containers' or 'gke' key not found in data.json.")
    st.stop()

azure_vcpu_price_per_second = azure_data['vcpu_price_per_second']
azure_gib_price_per_second = azure_data['gib_price_per_second']
gke_vcpu_price_per_second = gke_data['vcpu_price_per_second']
gke_gib_price_per_second = gke_data['gib_price_per_second']

# Sliders
vcpus = st.slider('vCPUs', 2, 8, 2)
gibs = st.slider('GiBs', 8, 24, 8)
minutes = st.slider('Minutes', 1, 480, 60)
number_of_tasks = st.slider('Number of Tasks', 1, 1000, 100)

# Calculation
number_of_seconds = minutes * 60
azure_usd_value = number_of_seconds * number_of_tasks * (azure_vcpu_price_per_second * vcpus + azure_gib_price_per_second * gibs)
gke_usd_value = number_of_seconds * number_of_tasks * (gke_vcpu_price_per_second * vcpus + gke_gib_price_per_second * gibs)

# Textboxes
st.subheader('Estimated Cost')
col1, col2 = st.columns(2)
with col1:
    st.text_input("Azure ContainerApps (USD)", value=f"{azure_usd_value:.2f}", disabled=True)
with col2:
    st.text_input("GKE (USD)", value=f"{gke_usd_value:.2f}", disabled=True)
