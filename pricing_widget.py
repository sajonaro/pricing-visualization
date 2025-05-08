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
cloudrun_data = pricing_data.get('gcp_cloudrun')
aws_lambda_data = pricing_data.get('aws_lambda')
cloud_functions_data = pricing_data.get('gcp_functions')
aws_app_runner_data = pricing_data.get('aws_app_runner')
aws_eks_fargate_data = pricing_data.get('aws_eks_fargate')

if not azure_data or not gke_data:
    st.error("Error: 'app_containers' or 'gke' key not found in data.json.")
    st.stop()

#azure container apps
azure_vcpu_pp_s = float(azure_data['vcpu_price_per_second'])
azure_gib_pp_s = float(azure_data['gib_price_per_second'])

#gke autopilot
gke_vcpu_pp_m = float(gke_data['vcpu_price_per_minute'])
gke_gib_pp_m = float(gke_data['gib_price_per_minute'])

#aws lambda
# Note: pricing data was taken for instance of 8GB RAM, for such instance the vCPU is 1
aws_lambda_gib_pp_s = float(aws_lambda_data['gib_price_per_second'])
aws_lambda_free_gibs_pp_s = float(aws_lambda_data['free_gib_seconds'])
aws_lambda_free_invocations = float(aws_lambda_data['free_invocations'])

#cloud run
cr_vcpu_pp_s = float(cloudrun_data['vcpu_price_per_second'])
cr_gib_pp_s = float(cloudrun_data['gib_price_per_second'])
cr_ft_gib_s = float(cloudrun_data['free_gib_seconds'])
cr_ft_vcpu_s = float(cloudrun_data['free_vcpu_seconds'])

#cloud run functions (previously gcp functions)
# Note: pricing data was taken fro 2 vcpus and 8192MB instance
crf_vcpu_pp_s = float(cloud_functions_data['vcpu_price_per_second'])
crf_ft_gib_s = float(cloud_functions_data['gibs_free_seconds'])
crf_ft_vcpu_s = float(cloud_functions_data['vcpus_free_seconds'])
cft_invocations = float(cloud_functions_data['free_invocations'])

# AWS cloud run 
aar_vcpu_pp_m= float(aws_app_runner_data['vcpu_price_per_minute'])
aar_gm_pp_m= float(aws_app_runner_data['gv_price_per_minute'])

#AWS EKS_Fargate
aws_eks_fargate_vcpu_pp_h = float(aws_eks_fargate_data['vcpu_price_per_hour'])
aws_eks_fargate_gib_pp_h = float(aws_eks_fargate_data['gv_price_per_hour'])

#AWS EKS_Fargate_Spot
aws_eks_fargate_spot_vcpu_pp_h = float(aws_eks_fargate_data['vcpu_price_per_hour_spot'])
aws_eks_fargate_spot_gib_pp_h = float(aws_eks_fargate_data['gv_price_per_hour_spot'])

# Sliders
vcpus = st.slider('vCPUs', 2, 8, 2)
gibs = st.slider('GiBs', 8, 24, 8)
mins = st.slider('Minutes each task runs', 1, 480, 60)
num_tasks = st.slider('Number of Tasks per invocation', 1, 1000, 100)
num_days = st.slider('Number of Days', 1, 31, 1)
invocations_per_day = st.slider('Invocations per day', 1, 10000, 1000)

secs = mins * 60
total_secs = num_tasks * secs * num_days
total_mins = total_secs / 60
total_invocations = invocations_per_day * num_tasks * num_days

# Calculation

azure_usd_value = total_secs * (azure_vcpu_pp_s * vcpus + azure_gib_pp_s * gibs)

gke_usd_value = num_days * mins * num_tasks * (gke_vcpu_pp_m * vcpus + gke_gib_pp_m * gibs)

aws_lambda_usd_value = 0 if total_invocations < aws_lambda_free_invocations else 8 *  aws_lambda_gib_pp_s  * total_secs - aws_lambda_free_gibs_pp_s * total_secs

cloudrun_usd_value =  (total_secs - cr_ft_vcpu_s/vcpus)*(cr_vcpu_pp_s * vcpus)  + (total_secs - cr_ft_gib_s/gibs)*(cr_gib_pp_s * gibs)

cloud_func_usd_value = 0 if total_invocations < cft_invocations else (total_secs - crf_ft_vcpu_s/2)*(crf_vcpu_pp_s * 2)  

aar_usd_value = total_mins*(aar_vcpu_pp_m * vcpus + aar_gm_pp_m * gibs)

awseksf_usd_value = total_secs * (aws_eks_fargate_vcpu_pp_h * vcpus + aws_eks_fargate_gib_pp_h * gibs) / 3600

awseksf_spot_usd_value = total_secs * (aws_eks_fargate_spot_vcpu_pp_h * vcpus + aws_eks_fargate_spot_gib_pp_h * gibs) / 3600


# Textboxes
st.subheader('Estimated Cost')
st.text_input("Azure Container Apps (USD)", value=f"{azure_usd_value:.2f}", disabled=True)
st.text_input("GKE (USD)                    ", value=f"{gke_usd_value:.2f}", disabled=True)
st.text_input("AWS Lambda (USD)             ", value=f"{aws_lambda_usd_value:.2f}", disabled=True)
st.text_input("GCP Cloud run (USD)          ", value=f"{cloudrun_usd_value:.2f}", disabled=True)
st.text_input("GCP Cloud run functions (USD)", value=f"{cloud_func_usd_value:.2f}", disabled=True)
st.text_input("AWS App run (USD)", value=f"{aar_usd_value:.2f}", disabled=True)
st.text_input("AWS EKS Fargate  (USD)", value=f"{awseksf_usd_value:.2f}", disabled=True)
st.text_input("AWS EKS Fargate Spot  (USD)", value=f"{awseksf_spot_usd_value:.2f}", disabled=True)



import matplotlib.pyplot as plt

# Pie chart data
labels = 'AZ container apps', 'GKE Autopilot', 'AWS Lambda', 'GCP Cloud Run', 'GCP Cloud Functions','AWS App Run', 'AWS EKS Fargate', 'AWS EKS Fargate Spot'
sizes = [azure_usd_value, gke_usd_value, aws_lambda_usd_value, cloudrun_usd_value, cloud_func_usd_value,aar_usd_value,awseksf_usd_value, awseksf_spot_usd_value]

# Create a pie chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the chart in Streamlit
st.subheader('Cost Comparison')
st.pyplot(fig1)

# Textboxes
st.subheader('Total seconds ran')
st.text_input("", value=f"{total_secs}", disabled=True)
