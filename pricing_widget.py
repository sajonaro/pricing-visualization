import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
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
gke_standard_data    = pricing_data.get('gke_standard')
azure_func_data      = pricing_data.get('azure_functions')
aks_standard_data    = pricing_data.get('aks_standard')

if not azure_data or not gke_autopilot_data or not cloudrun_data or not aws_lambda_data or not cloud_functions_data or not aws_app_runner_data or not aws_eks_fargate_data:
    st.error("Error: 'app_containers' or 'gke' or 'cloudrun' or 'aws_lambda' or 'cloud_functions' or 'aws_app_runner' or 'aws_eks_fargate' key not found in data.json.")
    st.stop()

#azure container apps
azure_vcpu_pp_s  = float(azure_data['vcpu_price_per_second'])
azure_gib_pp_s   = float(azure_data['gib_price_per_second'])

#gke standard
gke_pp_h      = float(gke_standard_data['price_per_hour'])
gke_pool_size = float(gke_standard_data['node_pool_size'])
gke_pp_h_spot = float(gke_standard_data['price_per_hour_spot'])

#aks standard
aks_pp_h      = float(aks_standard_data['price_per_hour'])
aks_pool_size = float(aks_standard_data['node_pool_size'])
aks_pp_h_spot = float(aks_standard_data['price_per_hour_spot'])  

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

#azure functions
azure_func_gibs_pp_s        = float(azure_func_data['gib_price_per_second'])
azure_func_free_gibs_pp_s   = float(azure_func_data['free_gib_seconds'])

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
aar_vcpu_pp_h   = float(aws_app_runner_data['vcpu_price_per_hour'])
aar_gb_pp_h     = float(aws_app_runner_data['gib_price_per_hour'])

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
 
# Pricing calculations

azure_container_apps_usd = total_secs * (azure_vcpu_pp_s  * vcpus + azure_gib_pp_s * gibs)
gke_autopilot_usd        = total_secs * (gke_vcpu_pp_h / 3600 * vcpus + gke_gib_pp_h / 3600 * gibs)
gke_autopilot_spot_usd   = total_secs * (gke_vcpu_pp_h_spot / 3600 * vcpus + gke_gib_pp_h_spot / 3600 * gibs)
aws_eksf_usd             = total_secs * (aws_eks_fargate_vcpu_pp_h / 3600 * vcpus + aws_eks_fargate_gib_pp_h / 3600 * gibs) 
aws_eksf_spot_usd        = total_secs * (aws_eks_fargate_spot_vcpu_pp_h / 3600 * vcpus + aws_eks_fargate_spot_gib_pp_h / 3600 * gibs) 
# NOTE, we don't count free invocations, neither for AWS Lambda nor Cloud Run Functions, it is much lover than compute price
aws_lambda_usd           = max( 8 * aws_lambda_gib_pp_s * (total_secs - aws_lambda_free_gibs_pp_s/8),0)

# NOTE, COnsumption plan serverless allows ONLY 1.5GB allocated per execution
azure_funcs_usd          = max( 1.5 * azure_func_gibs_pp_s * (total_secs - azure_func_free_gibs_pp_s/8),0)
# GCP pricing page says "free tier includes X GB-seconds and Y vCPU-seconds"  
# - this is BS! Actually it is EITHER X or Y, i.e. whatever runs out first, then immediately every second is billed!
cloudrun_usd             = max((total_secs - min(cr_ft_vcpu_s / vcpus, cr_ft_gib_s / gibs)) * (cr_vcpu_pp_s * vcpus + cr_gib_pp_s * gibs), 0)
cloud_func_usd           = max(crf_compute_pp_s * (total_secs - min(crf_ft_vcpu_s/2,crf_ft_gib_s/8)), 0)
# NOTE only 4 vcpu 8GB instance is available 
app_run_usd              = total_secs * (aar_vcpu_pp_h / 3600 * 4 + aar_gb_pp_h / 3600 * 8)

# NOTE
# 1: This is rough estimate, as scaling in and out of the node pool is not happening instantly (so effective price will be higher)
# 2: Also, additional research required to determine ideal  pod density (i.e pods per node) and CPU / RAM ratio of the working nodes in the pool (as general guidance the bigger (RAM) nodes perform better for memory bound tasks )
# 3: Also, we assume the whole cluster works for twice the average task execution time per invocation (could be optimized)
cluster_working_time_minutes = num_days * invocations_per_day * (2 * mins) * gke_pool_size
gke_standard_usd             = cluster_working_time_minutes * gke_pp_h / 60
gke_standard_spot_usd        = cluster_working_time_minutes * gke_pp_h_spot / 60


aks_standard_usd             = cluster_working_time_minutes * aks_pp_h / 60
aks_standard_spot_usd        = cluster_working_time_minutes * aks_pp_h_spot / 60

# Textboxes for tracing data
st.subheader('Execution stats:')

# Create columns
col1, col2  = st.columns(2)

# Place text inputs in columns
with col1:
    st.text_input("Effective total time (HH:MM:SS)", value=f"{total_secs // 3600:02d}:{(total_secs % 3600) // 60:02d}:{total_secs % 60:02d}", disabled=True)
with col2:
    st.text_input("Total invocations", value=f"{total_invocations}", disabled=True)


# Pie chart data
labels = (
    'AZ ContainerApps',
    'GKE Autopilot',
    'GKE Autopilot Spot',
    'GKE Standard',
    'GKE Standard Spot',
    'GCP Cloud Run',
    'GCP Functions',
    'AWS App Run',
    'AWS EKS Fargate',
    'AWS EKS Fargate Spot',
    'AWS Lambda',
    'Azure functions',
    "AKS Standard",
    "AKS Standard Spot"
)
sizes = [azure_container_apps_usd,
         gke_autopilot_usd,
         gke_autopilot_spot_usd,
         gke_standard_usd,
         gke_standard_spot_usd,   
         cloudrun_usd,
         cloud_func_usd,
         app_run_usd,
         aws_eksf_usd,
         aws_eksf_spot_usd,
         aws_lambda_usd,
         azure_funcs_usd,
         aks_standard_usd,
         aks_standard_spot_usd
         ]

# Calculate relative percentages
total_size = sum(sizes)
relative_percentages = [f"{label} ({size / total_size * 100:.1f}%)" for label, size in zip(labels, sizes)]

# Sort labels and sizes by relative percentage
sorted_labels_and_sizes = sorted(zip(labels, sizes), key=lambda x: x[1] / total_size * 100)

# Create a pie chart
fig1, ax1 = plt.subplots()
colors = plt.cm.rainbow(np.linspace(0, 1, len(sizes)))
ax1.pie([size for _, size in sorted_labels_and_sizes], colors=colors, shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# Add a legend
ax1.legend([f"{label} ({size / total_size * 100:.1f}%)" for label, size in sorted_labels_and_sizes], loc="upper right", bbox_to_anchor=(1.5, 1))

# Display the chart in Streamlit
st.subheader('Cost Comparison')
st.pyplot(fig1)

# Textboxes for pricing data
st.subheader('Estimated Cost Details by Service:')
st.caption('In ascending order of cost')
usd_values = [
    ("Azure Container Apps (USD)", azure_container_apps_usd),
    ("GKE Standard (USD)", gke_standard_usd),
    ("GKE Standard Spot(USD)", gke_standard_spot_usd),
    ("GKE Autopilot (USD)", gke_autopilot_usd),
    ("GKE Autopilot Spot", gke_autopilot_spot_usd),
    ("AWS Lambda (USD)", aws_lambda_usd),
    ("GCP Cloud run (USD)", cloudrun_usd),
    ("GCP Cloud run functions (USD)", cloud_func_usd),
    ("AWS App run (USD)", app_run_usd),
    ("AWS EKS Fargate  (USD)", aws_eksf_usd),
    ("AWS EKS Fargate Spot  (USD)", aws_eksf_spot_usd),
    ("Azure functions, on demand (USD)", azure_funcs_usd),
    ("AKS Standard (USD)", aks_standard_usd),
    ("AKS Standard Spot (USD)", aks_standard_spot_usd)
]

sorted_usd_values = sorted(usd_values, key=lambda x: x[1])

for i, (label, value) in enumerate(sorted_usd_values, start=1):
    st.write(f"{i}. {label}:")
    st.text_input("", value=f"{value:.2f}", disabled=True)