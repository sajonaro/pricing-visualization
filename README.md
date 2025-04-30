
##  widget to calculate cluster price



### Kubernetes Service Modes Across Major Cloud Providers

| Cloud Provider     | Service Name                     | Autopilot (No Node Management) | Standard                |
|--------------------|-----------------------------------|---------------------------------|-------------------------|
| Microsoft Azure    | Azure Kubernetes Service (AKS)   | Automatic (preview)            | Standard Mode           |
| Google Cloud (GCP) | Google Kubernetes Engine (GKE)   | Autopilot                      | Standard Mode           |
| Amazon Web Services (AWS) | Elastic Kubernetes Service (EKS) | Auto Mode                      | Standard Mode           |
| IBM Cloud          | IBM Kubernetes Service           | Not Available                  | Standard Mode           |
| Oracle Cloud       | Container Engine for Kubernetes (OKE) | Not Available                  | Standard Mode           |








Summary details and links to Kubernetes (flavors) and pricing info 
- Azure container apps [here](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
- Azure AKS 
    - Automatic (preview)
    - Standard mode cluster [pricing](https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/?msockid=173f6a45c2db68ed1d077ed6c39969c9#pricing)
    - VM [pricing](https://instances.vantage.sh/azure/vm/f72s-v2), e.g. compute optimized F series

- GKE 
    - Standard mode [VM prices](https://cloud.google.com/compute/vm-instance-pricing)
    - Autopilot Mode ( ! No ability to manage node pools!),  us-west-2 [here](https://cloud.google.com/kubernetes-engine/pricing#enterprise_edition)
- linode LKE [here](https://www.linode.com/pricing/#kubernetes)

AWS
 - EKS Auto Mode (AWS provisions and manages EC2 instances), [price example](https://instances.vantage.sh/aws/ec2/c6i.32xlarge), price = ec2 per hour + [EKS Auto Mode prices](https://aws.amazon.com/eks/pricing/) per hour 

 - EKS Standard Mode ( a.k.a Worker Nodes), price = EC2 + `small fees` , [example c6i.32xlarge](https://instances.vantage.sh/aws/ec2/c6i.32xlarge)






### Comparison of VM Instances Across Cloud Providers

| Instance Type    | vCPUs | RAM (GiB) | Price (On-Demand) | Cloud Provider     |
|------------------|-------|-----------|-------------------|--------------------|
| Standard_F72s_v2 | 72    | 144       | $3.04/hour        | Azure              |
| c6i.32xlarge      | 128   | 256       | $5.44/hour        | AWS                |
| m6i.24xlarge      | 96    | 384       | $4.75/hour        | AWS                |
| n2-highcpu-72     | 72    | 64        | $2.294/hour       | Google Cloud (GCP) |




## running the widget 


```bash
# to run tre widget
$ streamlit run pricing_widget.py
```