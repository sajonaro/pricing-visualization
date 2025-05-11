import streamlit as st
import matplotlib.pyplot as plt
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

## Note: 
# 1 Pricing data was taken for California North (i.e. relatively expensive region)
# 2 Price was taken for 2 vCPUs and 8192MB instance (whenever such instance was available)
azure_data           = pricing_data.get('app_containers')
gke_autopilot_data   = pricing_data.get('gke_autopilot')
cloudrun_data        = pricing_data.get('gcp_cloudrun')
aws_lambda_data      = pricing_data.get('aws_lambda')
cloud_functions_data = pricing_data.get('gcp_functions')
aws_app_runner_data  = pricing_data.get('aws_app_runner')
aws_eks_fargate_data = pricing_data.get('aws_eks_fargate')

if not azure_data or not gke_autopilot_data or not cloudrun_data or not aws_lambda_data or not cloud_functions_data or not aws_app_runner_data or not aws_eks_fargate_data:
    st.error("Error: 'app_containers' or 'gke' or 'cloudrun' or 'aws_lambda' or 'cloud_functions' or 'aws_app_runner' or 'aws_eks_fargate' key not found in data.json.")
    st.stop()

#azure container apps
azure_vcpu_pp_h  = float(azure_data['vcpu_price_per_hour'])
azure_gib_pp_h   = float(azure_data['gib_price_per_hour'])

#gke autopilot
gke_vcpu_pp_h   = float(gke_autopilot_data['vcpu_price_per_hour'])
gke_gib_pp_h    = float(gke_autopilot_data['gib_price_per_hour'])

#gke autopilot spot
gke_vcpu_pp_h_spot  = float(gke_autopilot_data['vcpu_price_per_hour_spot'])
gke_gib_pp_h_spot   = float(gke_autopilot_data['gib_price_per_hour_spot'])

#aws lambda
# Note: pricing data was taken for instance of 8GB RAM, for such instance the vCPU is to 2 (automatically, because it is > 1784MB)
aws_lambda_gib_pp_s         = float(aws_lambda_data['gib_price_per_second'])
aws_lambda_free_gibs_pp_s   = float(aws_lambda_data['free_gib_seconds'])
aws_lambda_free_invocations = float(aws_lambda_data['free_invocations'])

#cloud run
cr_vcpu_pp_s    = float(cloudrun_data['vcpu_price_per_second'])
cr_ft_gib_s     = float(cloudrun_data['free_gib_seconds'])
cr_ft_vcpu_s    = float(cloudrun_data['free_vcpu_seconds'])
cr_gib_pp_s     = float(cloudrun_data['gib_price_per_second'])

#cloud run functions (previously gcp functions)
# Note: pricing data was taken fro 2 vcpus and 8192MB instance
crf_compute_pp_s   = float(cloud_functions_data['vcpu_price_per_second'])
crf_ft_vcpu_s      = float(cloud_functions_data['vcpus_free_seconds'])
crf_ft_gib_s       = float(cloud_functions_data['gibs_free_seconds'])


# AWS cloud run 
aar_vcpu_pp_m   = float(aws_app_runner_data['vcpu_price_per_minute'])
aar_gm_pp_m     = float(aws_app_runner_data['gv_price_per_minute'])

#AWS EKS_Fargate
aws_eks_fargate_vcpu_pp_h   = float(aws_eks_fargate_data['vcpu_price_per_hour'])
aws_eks_fargate_gib_pp_h    = float(aws_eks_fargate_data['gv_price_per_hour'])

#AWS EKS_Fargate_Spot
aws_eks_fargate_spot_vcpu_pp_h  = float(aws_eks_fargate_data['vcpu_price_per_hour_spot'])
aws_eks_fargate_spot_gib_pp_h   = float(aws_eks_fargate_data['gv_price_per_hour_spot'])

# Sliders
vcpus               = st.slider('vCPUs', 2, 8, 2)
gibs                = st.slider('GiBs', 8, 24, 8)
invocations_per_day = st.slider('Invocations per day', 1, 200, 20)
mins                = st.slider('Minutes each task runs', 1, 120, 8)
num_tasks           = st.slider('Number of Tasks per invocation', 1, 2000, 1000)
num_days            = st.slider('Number of Days', 1, 31, 25)



# Calculations

total_invocations = invocations_per_day * num_tasks * num_days
total_mins        = total_invocations * mins 
total_secs        = total_mins * 60
total_hours       = total_mins / 60
 
# Pricing calculations

azure_container_apps_usd = total_hours * (azure_vcpu_pp_h * vcpus + azure_gib_pp_h * gibs)
gke_autopilot_usd        = total_hours * (gke_vcpu_pp_h * vcpus + gke_gib_pp_h * gibs)
gke_autopilot_spot_usd   = total_hours * (gke_vcpu_pp_h_spot * vcpus + gke_gib_pp_h_spot * gibs)
aws_eksf_usd             = total_hours * (aws_eks_fargate_vcpu_pp_h * vcpus + aws_eks_fargate_gib_pp_h * gibs) 
aws_eksf_spot_usd        = total_hours * (aws_eks_fargate_spot_vcpu_pp_h * vcpus + aws_eks_fargate_spot_gib_pp_h * gibs) 
cloudrun_usd             = (total_secs - cr_ft_vcpu_s/vcpus)*(cr_vcpu_pp_s * vcpus)  + (total_secs - cr_ft_gib_s/gibs)*(cr_gib_pp_s * gibs)
# Note, we don't count free invocations, neither for AWS Lambda nor Cloud Run Functions, it is much lover than compute price
aws_lambda_usd           = max( aws_lambda_gib_pp_s * (total_secs - aws_lambda_free_gibs_pp_s/8),0)
# GCP pricing page says "free tier includes X GB-seconds and Y vCPU-seconds"  
# - this is BS, actually it is EITHER X or Y,
#  moreover whatever runs out first!
cloud_func_usd           = max( crf_compute_pp_s * (total_secs - min(crf_ft_vcpu_s/2,crf_ft_gib_s/8)),0) 
app_run_usd              = total_mins * (aar_vcpu_pp_m * vcpus + aar_gm_pp_m * gibs)


# Textboxes for tracing data

st.subheader('Total execution stats:')

# Create columns
col1, col2, col3 = st.columns(3)

# Place text inputs in columns
with col1:
    st.text_input("Total seconds", value=f"{total_secs}", disabled=True)
with col2:
    st.text_input("Total hours", value=f"{total_mins }", disabled=True)
with col3:
    st.text_input("Total invocations", value=f"{total_invocations}", disabled=True)


# Pie chart data
labels = 'AZ ContainerApps', 'GKE Autopilot', 'GKE Autopilot Spot','AWS Lambda', 'GCP Cloud Run', 'GCP Functions','AWS App Run', 'AWS EKS Fargate', 'AWS EKS Fargate Spot'
sizes = [azure_container_apps_usd,
         gke_autopilot_usd,
         gke_autopilot_spot_usd,
         aws_lambda_usd,
         cloudrun_usd,
         cloud_func_usd,
         app_run_usd,
         aws_eksf_usd,
         aws_eksf_spot_usd]

# Calculate relative percentages
total_size = sum(sizes)
relative_percentages = [f"{label} ({size / total_size * 100:.1f}%)" for label, size in zip(labels, sizes)]

# Create a pie chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, shadow=False, startangle=90 )
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# Add a legend
ax1.legend(relative_percentages, loc="upper right", bbox_to_anchor=(1.5, 1))

# Display the chart in Streamlit
st.subheader('Cost Comparison')
st.pyplot(fig1)

# Textboxes for pricing data
st.subheader('Estimated Cost Details by Service')

st.text_input("Azure Container Apps (USD)",     value=f"{azure_container_apps_usd:.2f}", disabled=True)
st.text_input("GKE Autopilot (USD)",            value=f"{gke_autopilot_usd:.2f}", disabled=True)
st.text_input("GKE Autopilot Spot",             value=f"{gke_autopilot_spot_usd:.2f}", disabled=True)
st.text_input("AWS Lambda (USD)",               value=f"{aws_lambda_usd:.2f}", disabled=True)
st.text_input("GCP Cloud run (USD)",            value=f"{cloudrun_usd:.2f}", disabled=True)
st.text_input("GCP Cloud run functions (USD)",  value=f"{cloud_func_usd:.2f}", disabled=True)
st.text_input("AWS App run (USD)",              value=f"{app_run_usd:.2f}", disabled=True)
st.text_input("AWS EKS Fargate  (USD)",         value=f"{aws_eksf_usd:.2f}", disabled=True)
st.text_input("AWS EKS Fargate Spot  (USD)",    value=f"{aws_eksf_spot_usd:.2f}", disabled=True)