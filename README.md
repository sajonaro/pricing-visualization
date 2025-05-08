
##  widget to calculate cluster price



### Managed Kubernetes modes across major cloud providers

| Cloud Provider     | Service Name                     | Autopilot (No Node Management) | Standard                |
|--------------------|----------------------------------|--------------------------------|-------------------------|
| Microsoft Azure    | Azure Kubernetes Service (AKS)   | Automatic (preview)            | Standard Mode           |
| Google Cloud (GCP) | Google Kubernetes Engine (GKE)   | Autopilot                      | Standard Mode           |
| Amazon Web Services (AWS) | Elastic Kubernetes Service (EKS) | Auto Mode               | Standard Mode           |
| IBM Cloud          | IBM Kubernetes Service           | Not Available                  | Standard Mode           |
| Oracle Cloud       | Container Engine for Kubernetes (OKE) | Not Available             | Standard Mode           |

### Serverless options 
| Provider      | Service Name           | Backing Tech          | Abstraction Level | Use Case                                      | Pricing Model                       |
|---------------|------------------------|-----------------------|-------------------|-----------------------------------------------|-------------------------------------|
| Google Cloud  | Cloud Run              | Knative               | High              | Stateless HTTP containers                      | Per request + CPU/Memory per sec  [link to pricing](https://cloud.google.com/run/pricing) |
| AWS           | App Runner             | AWS-managed           | High              | Web services, APIs from container images       | Per request + CPU/Memory per sec, [link to pricing](https://aws.amazon.com/apprunner/pricing/)   |
| Azure         | Azure Container Apps   | Kubernetes + KEDA     | High              | Event-driven or HTTP microservices             | Per request + CPU/Memory per sec, [link to pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)   |
| Azure         | AKS with Virtual Nodes | Kubernetes (AKS + ACI)| Medium           | Burst workloads in Kubernetes                  | Per vCPU/Memory (ACI pricing)       |
| Google Cloud  | GKE Autopilot          | Kubernetes            | Medium            | Kubernetes apps without node management        | Per pod vCPU/Memory usage          |
| AWS           | AWS Fargate (with EKS) | Kubernetes (EKS)      | Medium            | Run pods without managing EC2 nodes            | Per vCPU and memory per second   [link to pricing](https://aws.amazon.com/fargate/pricing/)  |



### Strategies for cost optimization 
 - GKE
    - Autopilot + SpotInstances (60-90 % discount for VMs), CUD (Committed Usage Discount)
    - Standard Mode + Kubernetes Autoscaler 


- AWS Karpenter (with Spot instances)






Summary details and links to Kubernetes (flavors) and pricing info 
- Azure container apps [here](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
- Azure AKS 
    - Automatic (preview)
    - Standard mode cluster [pricing](https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/?msockid=173f6a45c2db68ed1d077ed6c39969c9#pricing)
    - VM [pricing](https://instances.vantage.sh/azure/vm/f72s-v2), e.g. compute optimized F series
- GCP
    - Cloud Run Functions, price = compute - free tier  [compute prices, 1st](https://cloud.google.com/functions/pricing-1stgen)
    - Cloud Run,  price = compute + memory + (flat) invocation - free tier [pricing](https://cloud.google.com/run/pricing)
    - GKE 
        - Standard mode [VM prices](https://cloud.google.com/compute/vm-instance-pricing)
        - Autopilot Mode ( ! No ability to manage node pools!),  us-west-2 [here](https://cloud.google.com/kubernetes-engine/pricing#autopilot_mode)
- linode LKE [here](https://www.linode.com/pricing/#kubernetes)

AWS
 - EKS Auto Mode (AWS provisions and manages EC2 instances), [price example](https://instances.vantage.sh/aws/ec2/c6i.32xlarge), price = ec2 per hour + [EKS Auto Mode prices](https://aws.amazon.com/eks/pricing/) per hour 

 - EKS Standard Mode ( a.k.a Worker Nodes), price = EC2 + `small fees` , [example c6i.32xlarge](https://instances.vantage.sh/aws/ec2/c6i.32xlarge)

 - Lambdas, price  = compute + (flat) invocation,  [compute prices](https://aws.amazon.com/lambda/pricing/) 




### Comparison of VM Instances Across Cloud Providers

| Instance Type    | vCPUs | RAM (GiB) | Price (On-Demand) | Cloud Provider     |
|------------------|-------|-----------|-------------------|--------------------|
| Standard_F72s_v2 | 72    | 144       | $3.04/hour        | Azure              |
| c6i.32xlarge      | 128   | 256       | $5.44/hour        | AWS                |
| m6i.24xlarge      | 96    | 384       | $4.75/hour        | AWS                |
| n2-highcpu-72     | 72    | 64        | $2.294/hour       | Google Cloud (GCP) |




## running the widget 


```bash
# to run the widget
$ make run
```

```bash
# to stop the widget
$ make kill
```