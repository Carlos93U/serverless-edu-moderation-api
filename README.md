# Serverless Edu Moderation API

A serverless image‐moderation API for educational platforms, built with **AWS Rekognition**, **Lambda**, **API Gateway**, and **Terraform**. It automatically detects unsafe or inappropriate content to maintain a secure learning environment.

---

## 1. Goal

The goal is to automatically evaluate uploaded images and determine whether they are safe for use in school or academic environments. The system analyzes images using **Amazon Rekognition Moderation Labels** and classifies them into three categories:

- **LOW Risk** → ACCEPTED
- **HIGH Risk** → REJECTED

---

## 2. Use Case: Educational Platform Moderation

This API integrates with LMS systems (Moodle, Blackboard, Google Classroom clones, etc.) to:

- Validate **student profile photos**
- Moderate **uploaded assignments**
- Review **forum & chat images**
- Protect minors from exposure to harmful material

---

## 3. Architecture

The architecture follows the same principles from the chapter's serverless solution, updated for content moderation:

<p align="center">
  <img src="assets/arch.gif" alt="Architecture Diagram">
</p>

To se Detailed flow description and examples for each step, go to [architecture partern file](./assets/architecture_pattern.md)

## 4. Features

- Serverless and pay‑per‑use
- Moderation label detection using Rekognition
- Accepts base64‑encoded images
- Returns structured JSON for frontend or backend systems

---

## 5. How It Works

### **5.1. Requirements Definition**

- Must detect inappropriate image content
- Must not store personal images
- Must handle multiple client apps
- Must be low‑cost and scalable

### **5.2. Architecture Selection**

Chosen approach: **pre‑trained managed model with Amazon Rekognition**.

### **5.3. Infrastructure Deployment (Terraform)**

Terraform provisions:

- Lambda function
- IAM roles with Rekognition & CloudWatch permissions
- REST API Gateway
- Lambda permissions for invocation

### **5.4. Lambda Implementation (Python)**

- Accepts base64 payload
- Calls Rekognition DetectModerationLabels
- Applies risk‑classification logic
- Returns JSON response

### **5.5. Testing Locally**

You may test via:

- Running the handler locally
- Using AWS SAM CLI
- Sending requests through Postman with base64 images

### **5.6. Deployment**

Run:

```
terraform apply
```

Terraform outputs the API invoke URL.

---

## 6. Project Folder Structure

A clean and organized structure adapted for Terraform + Lambda:

```
serverless-edu-moderation-api/
├── terraform/
│   ├── lambda.tf
│   ├── dns.tf
│   ├── apigw.tf
│   ├── variables.tf
│   ├── terraform.tfvars
├── python/
│   ├── moderation.py
│   └── moderation.zip   (auto‑generated)
├── assets/
│   ├── arch.gif
│   ├── architecture_pattern.md
│   ├── hate_symb.png
│   ├── machu_picchu.png
│   └── pricing_calculations.pdf
├── README.md
└── .gitignore
```

---

## 7. Deploying with Terraform

Follow these steps to deploy the API into AWS.

### **7.1. Configure AWS credentials**

Ensure AWS CLI is authenticated:

```bash
aws configure
```

### **7.2. Navigate to the Terraform directory**

```bash
cd terraform
```

### **7.3. Initialize Terraform**

```bash
terraform init
```

### **7.4. Validate configuration**

```bash
terraform validate
```

### **7.5. Deploy infrastructure**

```bash
terraform apply
```

Confirm with **yes** when prompted.

### **7.6. Retrieve API URL**

Terraform will output something like:

```
https://abcd1234.execute-api.us-east-1.amazonaws.com/dev/moderate
```

This is your production endpoint.

### **7.7. Test the deployed API using interact.py**

Once deployed, you can test the API using the provided `interact.py` script. This script sends an image to your API Gateway endpoint and displays the moderation results.

**Usage:**

```bash
python3 interact.py <api_gateway_url> <image_path>
```

**Example:**

```bash
python3 interact.py https://abcd1234.execute-api.us-east-1.amazonaws.com/dev/moderate assets/machu_picchu.png
```

**Expected output for a safe image:**

```json
Good Profile Photo
```

**Test with different images:**

```bash
# Test with a safe image
python3 interact.py <your-api-url> assets/machu_picchu.png

# Test with inappropriate content
python3 interact.py <your-api-url> assets/hate_symb.png
```



### **7.8. Destroy resources when done**

To delete all the resources you just created, run:

```bash
terraform destroy
```

---

## 8. Estimated Monthly Costs

The following table summarizes the estimated monthly costs for this architecture assuming an average of **9,000 image moderation inferences per month** (based on 200 students uploading 2 images per day, 5 days per week, plus a 1,000-image buffer).

### **8.1. Amazon Rekognition – Content Moderation**
- Pricing: **$0.0010 USD per image**
- Calculation:
  ```
  9,000 images × $0.0010 = $9.00 USD/month
  ```

### **8.2. AWS Lambda**
Assumptions:
- 128 MB memory  
- ~250 ms average execution  
- 9,000 invocations per month  
- Lambda free tier covers the first 1M requests  

Compute cost:
```
Cost per execution ≈ $0.00000052
9,000 executions ≈ $0.00468 USD/month
```
Total Lambda cost: **~$0.005 USD/month**

### **8.3. Amazon API Gateway (REST API)**
- Pricing: **$3.50 per 1 million requests**
- Calculation:
  ```
  9,000 requests ≈ 0.009M
  0.009 × $3.50 = $0.0315 USD/month
  ```

---

## **9. Monthly Cost Summary**

| Service                    | Unit Price                     | Monthly Usage | Estimated Monthly Cost |
|----------------------------|--------------------------------|---------------|--------------------------|
| **Rekognition (Moderation)** | $0.0010 per image              | 9,000 images  | **$9.00**                |
| **AWS Lambda**              | ~$0.00000052 per invocation    | 9,000 calls   | **$0.005**               |
| **API Gateway (REST)**      | $3.50 per 1M requests          | 9,000 calls   | **$0.03**                |
| **Total Estimated Cost**    | —                              | —             | **~$9.03 USD/month**     |

If you check this calculos go to AWS princing calculator link fot this project 
- [Check Calculus](https://calculator.aws/#/estimate?id=c7d02b80e9e0a056c0a1c440bd131cd826209091)

## **10. Summary**
The entire serverless content‑moderation pipeline operates for **under $10 USD per month**, with the vast majority of cost coming from **Rekognition**. Lambda and API Gateway contribute only a few cents.
