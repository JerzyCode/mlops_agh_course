# Lab 13 Report

## Setting up the Qwen HuggingFace transformers inference

It lasts a lot, but it returned response:

```md
 The importance of LLMOps (Large Language Model Operations) can be assessed on a scale of 0-10 based on its criticality to the success, reliability, and scalability of large language models (LLMs). Here's a structured breakdown:

### **Key Factors Influencing Importance (0-10):**
1. **Deployment & Integration (7/10):**  
   - **Criticality:** High. LLMOps is essential for deploying models into production environments, ensuring seamless integration with existing systems.  
   - **Why:** Without proper deployment, models risk being underutilized or causing operational disruptions.  

2. **Monitoring & Performance (8/10):**  
   - **Criticality:** Very High. Continuous monitoring ensures models maintain performance, detect issues (e.g., bias, hallucinations), and scale dynamically.  
   - **Why:** Models require real-time feedback to adapt to user needs and system changes.  

3. **Security & Compliance (8/10):**  
   - **Criticality:** High. Protecting data privacy, preventing adversarial attacks, and ensuring compliance with regulations (e.g., GDPR, HIPAA) is non-negotiable.  
   - **Why:** Security breaches can lead to reputational damage and legal penalties.  

4. **Scalability (9/10):**  
   - **Criticality:** Extremely High. LLMOps ensures models can handle massive data and user loads without degradation in performance.  
   - **Why:** Scalability is vital for businesses relying on LLMs for real-time applications (e.g., customer service, content generation).  

5. **Cost Efficiency (7/10):**  
   - **Criticality:** Moderate. Optimizing resource usage (e.g., GPU/TPU allocation) and reducing latency improves cost-effectiveness.  
   - **Why:** High costs can arise from inefficient scaling or poor model maintenance.  

6. **Innovation & Iteration (6/10):**  
   - **Criticality:** Moderate. LLMOps enables continuous updates and improvements, but this depends on the model's lifecycle and the organization's agility.  

### **Overall Importance (Combined):**  
- **8/10:** LLMOps is **crucial** for maintaining reliability, security, and scalability in production. It is a **core operational requirement** for businesses leveraging LLMs in critical applications.  
- **Reasoning:**  
  - **High stakes:** Models are often mission-critical (e.g., healthcare, finance, customer service).  
  - **Complexity:** Managing large, dynamic models requires specialized tools and expertise.  
  - **Regulatory and ethical concerns:** Compliance and fairness are paramount, adding layers of complexity.  

### **Conclusion:**  
LLMOps is **highly important** (8/10) for most organizations, especially those deploying LLMs at scale. Its role in ensuring reliability, security, and performance is indispensable. However, its importance may vary based on the specific use case, industry, and organizational maturity.  

**Final Score:** **8/10** (Highly Important)  
**Justification:** LLMOps is essential for operationalizing large language models, balancing technical, security, and business demands.
```


## vLLM inference

For the vllm, because of the lack of GPU, the athena.cyfronet was used. **The lab was done on A100 40GB**.

The setup was as follows:

```bash
uv init
uv add vllm

srun ... # for gpu

module load CUDA/12.8.0

export HF_HOME="" # to not overload $HOME dir

uv run vllm serve Qwen/Qwen3-1.7B --port 8000 --max-model-len 8192 --dtype bfloat16 --host 0.0.0.0
```

Then tunneling from local machine:

```
ssh -L 8000:node_id:8000 login@athena.cyfronet.pl
```


Everything is running, after running code form file `openai_inference.py` results:

```md
 **LLMOps (Large Language Model Operations)** is a critical component in the deployment and management of large language models (LLMs), and its importance can be measured on a scale from **0 to 10** as follows:

---

### **Scale 10: Essential and Critical**

**LLMOps is essential for the successful deployment and maintenance of large language models.** It provides the necessary infrastructure, monitoring, and automation to ensure that models are reliable, performant, and secure in production environments. Key reasons:

- **Model Stability:** LLMOps ensures that models are consistently trained, fine-tuned, and monitored for drift or degradation.
- **Scalability:** It enables the deployment of models at scale, handling large volumes of data and user interactions.
- **Security and Compliance:** LLMOps includes mechanisms for data protection, access control, and compliance with regulations.
- **Performance Optimization:** It helps in optimizing model performance, inference speed, and resource usage.
- **Feedback Loops:** It enables continuous feedback and iteration based on real-world usage.

---

### **Scale 9: Very Important**

**LLMOps is very important for large-scale deployment and maintaining model quality.** It supports:

- **Model Versioning and Rollbacks:** Ensures that models can be updated and rolled back if needed.
- **Monitoring and Logging:** Provides visibility into model behavior and performance.
- **Auto-Scaling:** Enables the model to scale with traffic and resource demands.
- **Cost Management:** Helps in managing costs associated with model inference and training.

---

### **Scale 8: Important but Not Mandatory**

**LLMOps is important but not mandatory for smaller models or in less complex environments.** It may be considered important in:

- **Model Development:** For iterative development and testing.
- **Training and Evaluation:** For managing training pipelines and evaluation metrics.
- **Data Governance:** For managing data quality and data pipelines.

---

### **Scale 7: Slightly Important**

**LLMOps is slightly important for some use cases, such as:**

- **Model Deployment in Specific Environments**
- **Customized Model Management**
- **Integration with Third-Party Systems**

---

### **Scale 6: Not Critical for Simple Use Cases**

**LLMOps is not critical for simple use cases where the model is small, not used in production, or not part of a complex pipeline.**

---

### **Summary Table: LLMOps Importance (Scale 0-10)**

| Scale | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| 0     | LLMOps is not required. Model is deployed without automation, monitoring, or management.                                 |
| 1     | LLMOps is minimal. Model is deployed manually with little to no automation.                                              |
| 2     | LLMOps is basic. Model is deployed with some automation, but not extensive.                                              |
| 3     | LLMOps is moderate. Model is deployed with some monitoring and basic automation.                                         |
| 4     | LLMOps is significant. Model is deployed with monitoring, logging, and basic automation.                                 |
| 5     | LLMOps is important. Model is deployed with monitoring, logging, and some automation.                                    |
| 6     | LLMOps is slightly important. Model is deployed with some monitoring and automation.                                     |
| 7     | LLMOps is important for some use cases. Model is deployed with monitoring and automation.                                |
| 8     | LLMOps is very important. Model is deployed with comprehensive monitoring, logging, and automation.                      |
| 9     | LLMOps is essential. Model is deployed with robust monitoring, logging, and automation.                                  |
| 10    | LLMOps is critical. Model is deployed with advanced monitoring, logging, and automation for scalability and reliability. |

---

### **Conclusion**

**LLMOps is most important on a scale of 9-10**, especially for large-scale, production-ready models. It is critical for ensuring model reliability, performance, and security in real-world environments. Without LLMOps, models can be unstable, inefficient, and difficult to manage in production.
```


With GPU of a100 it lasts for <1s.



## Exercise 1

Script for sending 10 requests is in the `run_prompts.py`.

**`Qwen/Qwen3-1.7B`**

| quantization             | total_time (s) | avg_time (s) | kv_cache_memory (GiB) | Model weight (GiB) |
| ------------------------ | -------------- | ------------ | --------------------- | ------------------ |
| float32                  | 38.47          | 3.85         | 27.92                 | 3.22               |
| bfloat16                 | 26.51          | 2.65         | 31.06                 | 3.22               |
| 4bit-quant  bitsandbytes | 24.41          | 2.44         | 32.95                 | 1.33               |


For the A100 GPU the speedup is not that significant, however it is noticeable. Probably that kind of gpu quantization of that small model `Qwen/Qwen3-1.7B` is overkill.

**`Qwen/Qwen3-14B`**

| quantization             | total_time (s) | avg_time (s) | kv_cache_memory (GiB) | Model weight (GiB) |
| ------------------------ | -------------- | ------------ | --------------------- | ------------------ |
| bfloat16                 | 135.57         | 13.56        | 6.66                  | 27.52              |
| 4bit-quant  bitsandbytes | 86.54          | 8.65         | 24.28                 | 9.9                |

As expected, the gain for larger scale model is more significant. Overall: quantization with bitsandbytes is "very strong".

For the rest of lab, the model `Qwen/Qwen3-1.7B` will be used with no quantization. The reason for that is to check if models of that size are capable of using tools.


## Manual tool calling

It works, logs for Birmingham:

```bash
jerzy-boksa@jerzyb-laptop:~/Programming/Projects/university/term_3/mlops_agh_course/lab13$ uv run tools_calling.py 
Generated message: {'content': None, 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': [{'id': 'chatcmpl-tool-8e8387279ea5936e', 'function': {'arguments': '{}', 'name': 'get_current_date'}, 'type': 'function'}], 'reasoning': None, 'reasoning_content': None}

Generated message: {'content': None, 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': [{'id': 'chatcmpl-tool-beaea2517fbcc9d8', 'function': {'arguments': '{"country": "United Kingdom", "city": "Birmingham", "date": "2026-01-21"}', 'name': 'get_weather_forecast'}, 'type': 'function'}], 'reasoning': None, 'reasoning_content': None}

Generated message: {'content': 'The weather in Birmingham, United Kingdom, on January 21, 2026, is expected to be fog and rain.', 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 'function_call': None, 'tool_calls': [], 'reasoning': None, 'reasoning_content': None}

Response:
 The weather in Birmingham, United Kingdom, on January 21, 2026, is expected to be fog and rain.
```
It was very fast.



## Exercise 2

The implemenation is in `exercise2/run_tools.py`.


### Question 1:
- What is included in the APIs Tox dataset?

**response:**

  The "APIs Tox" dataset contains information about APIs that have been identified as toxic or harmful. This dataset is typically used in the context of software development and testing to identify and evaluate the potential risks or issues associated with certain APIs. The specific details of the dataset may vary, but it generally includes data on the APIs' functionalities, potential risks, and other relevant characteristics.

### Question 2:
- What is SMILES of Ethanedioic acid and Calcium carbonate?
- 
**response:**

```md
 The SMILES (Shorter Molecular Initiative for Structure Representation) notation is a way to represent chemical molecules in a string format. Here are the SMILES for the compounds you asked about:

- **Ethanedioic acid**: `CC(=O)O`
- **Calcium carbonate**: `CaCO3`

These SMILES strings represent the molecular structures of the compounds in a standardized format.
```

### Question 3:
- What are the columns of taxi dataset?

**Response:**

```md
Response:
 The columns of the New York taxi dataset include:

- **VendorID**: Unique identifier for the vendor.
- **tpep_pickup_datetime**: The date and time when the pickup occurred.
- **tpep_dropoff_datetime**: The date and time when the dropoff occurred.
- **passenger_count**: Number of passengers in the taxi.
- **trip_distance**: Distance of the trip in miles.
- **RatecodeID**: Identifier for the rate code used.
- **store_and_fwd_flag**: Indicates if the taxi had to store and forward the bill.
- **PULocationID**: Location ID of the pickup location.
- **DOLocationID**: Location ID of the dropoff location.
- **payment_type**: Type of payment made (e.g., cash, credit card, etc.).
- **fare_amount**: Total fare amount.
- **extra**: Extra charges (e.g., airport fee, etc.).
- **mta_tax**: Tax applied by the MTA.
- **tip_amount**: Tip amount given by the passenger.
- **tolls_amount**: Toll charges.
- **improvement_surcharge**: Improvement surcharge.
- **total_amount**: Total amount paid for the trip.
- **congestion_surcharge**: Congestion surcharge (if applicable).
- **Airport_fee**: Airport fee (if applicable).
- **cbd_congestion_fee**: Congestion fee in the CBD (Central Business District).

Let me know if you need more details about any of these columns!
```