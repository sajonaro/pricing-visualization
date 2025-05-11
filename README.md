
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

#### Pricing references

More details are in `./data.json`, but below are some quick links
- [GCP GKE Autopilot](https://cloud.google.com/kubernetes-engine/pricing)
- [GCP Cloud Run, LA, ue-west-2](https://cloud.google.com/run/pricing#tables)
- [GCP Cloud Run Functions, (aka Functions)](https://cloud.google.com/functions/pricing-1stgen), 
- [AWS EKS Fargate](https://aws.amazon.com/fargate/pricing/)
- [Azure ContainerApps](https://azure.microsoft.com/en-us/pricing/details/container-apps/)


### Strategies for cost optimization

Data shows only { k8 } and {k8 + autopilot } are really viable options (cost efficiency wise).
So the exact tactics may be:
1. Using spot instances ( for both K8 and k8 + autopilot)
2. Using k8 with custom autoscaler e.g. Karpenter 
3. (Mutually exclusive to 2) Self manage node pool ( * experimenting with pod density,CPU/RAM ratio, VM size, utilization parameters to find optimal configuration )
4. Combination of above
5. Make sure to NOT use GKE Enterprise + Autopilot (use standard)
6. Prefer ARM vs x86 architectures (as it is marginally consistently cheaper)

#### TODO cost-efficiency / maintainability chart


### VM prices reference:
- [link to Azure](https://instances.vantage.sh/azure/vm/f72s-v2)
- [link to AWS](https://instances.vantage.sh/aws/ec2/c6i.32xlarge)
- [link to GCP](https://instances.vantage.sh/aws/ec2/c6i.32xlarge)

#### quick Comparison of VM Instances Across Cloud Providers
 
| Instance Type    | vCPUs | RAM (GiB) | Price (On-Demand) | Cloud Provider     |
|------------------|-------|-----------|-------------------|--------------------|
| Standard_F72s_v2 | 72    | 144       | $3.04/hour        | Azure              |
| c6i.32xlarge      | 128   | 256       | $5.44/hour        | AWS                |
| m6i.24xlarge      | 96    | 384       | $4.75/hour        | AWS                |
| n2-highcpu-72     | 72    | 64        | $2.294/hour       | Google Cloud (GCP) |

## How to run the widget 


```bash
# to run the widget
$ make run
```

```bash
# to stop the widget
$ make kill
```