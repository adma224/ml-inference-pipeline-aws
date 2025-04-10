# :poodle: Model Inference Pipeline with AWS CDK and CI/CD

## At its base...

#### News Headline Generator – GPT-2 Headline Completion Web App
This web application demonstrates a generative AI pipeline that completes partial news headlines, fully deployed on a serverless AWS architecture. Behind the scenes, two models handle inference requests in a 50/50 A/B split, with upvotes, downvotes, and other metadata collected for visualization and performance analysis.

The demo is still a work in progress and the model will generate quirky or unexpected headlines, but expected as it continues to improve.

## [Click for live demo here!](https://frontendstack-frontendbucketefe2e19c-uod6vgeirydc.s3.us-east-1.amazonaws.com/index.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIA5OWK4APTROBDYOXO%2F20250410%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250410T052833Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECYaCXVzLWVhc3QtMSJIMEYCIQD9rjDN1e3mCv%2BE2AOG%2BHRg1Hzdp%2FRNebVXMXIfcEk4ZwIhAKKpTB7JNnrjhWG%2BvZKaxip0vRqHRRnZ%2FVAlErZCARdnKuMCCJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMOTI0OTE3MTcxMTc1IgzvczDhrHWAMVoW%2BHwqtwIvDDhF7kdsPyPEpX93r9B9spAY2pSzBvRY0cwLwz9vVmPTkNKCBCpqd3aA98OhtPSWlCP4otZKGvYNieZyB2gCf9rlWELjC5tmjiKNqK9rQTkDqu3JoW2X6WjjVEyhKTcCh2XkOYQ6CsaChylb2kt69WqJXvC8PfM5Z9wtfOD%2FuKFOOAMWyStCUj%2FWprg6CQLaaZyaa2QHOnW2kVob%2FkmJXxMYmal3091YJTPQKN0ObrZAXwROwkot7KzXXhcOzc2jBzVDpcqwBJgFk1dZkyjVfvbZQKOn0Xjglhevvyi%2B%2BiBUVYOmA1t0CYlwX1KR9mkY7BcKXWn6aSVPfk5YT404IiYLDK1vkRuzCjok2kx5Iw8ghgnkyRkjQvKy5Zv6IOLCD1a%2Bua2nWyGgxt%2FGIb318Q4U5jlZ9TDord2%2FBjqsAtjORp2cnF7eD%2BL2jSDEoixCCyg9hrB5LvJc2hfRa7nQVigS5ylUFp%2B0lD%2Fr%2B2eshsPx38hhd1Xi3OAjUs%2FkoKFYA0Cx6U5KP%2BDFm7zPrKnWBKf1%2FeDS3mYlXF%2BF9R6ofC8OZ1utCn5fVgNcKX79gqMW%2FRgMOwQbOTHisTCF2tTK8qUQNvmd1w2UYupeycKFpdvMYircZV%2B2JaHsrHAokVjTF7tvh7iKxewlJHYbrt1HCegPaN5q95e%2FZZUZSXspDTmS2ktMxVMnX8pvTEr%2FJRtFcmWShcXRhcz3V2L7egulbR3q8SZ%2Fr7F0dd4kmNhf%2F2rbe8HpyYr53PQ8VL20nyaxXQlZHxUXcLQufx83kpPlCWdPZ6Zw0AdaguQSq0HXDi%2FYwgmycT%2F2DnYyvw%3D%3D&X-Amz-Signature=cfd03c112d6d8b5e66e35d4d0d6d03a8f0335f1f78ad88eb92e1d592f7d81ca1&X-Amz-SignedHeaders=host&response-content-disposition=inline)

*After clicking on "Generate", allow 5-15 seconds for the inference container to warm up (warming up mechanism coming soon)*

### ✏️ How it works

1. Type the beginning of a news headline (just a few words)
2. Click **Generate**
3. The app will return a completed headline based on your prompt

### 🧪 Example prompts

- `Scientists discover`
- `New law passed to`
- `AI could soon`
- `Stock market reacts`
---

## Project Description

This project demonstrates a scalable, production-style inference pipeline using AWS CDK, Lambda, API Gateway, and SageMaker. It includes a fully automated CI/CD pipeline powered by GitHub Actions and is designed to showcase mid-level skills in AWS Cloud Engineering, DevOps, Machine Learning Engineering, and MLOps.


[AWS Infrastructure Diagram](https://github.com/adma224/ml-inference-pipeline-aws/blob/main/diagrams/infrastructure_diagram_aws_ml_pipeline.png) - [GitHub Project Board](https://github.com/users/adma224/projects/7)


---

## Project Goals

- Deploy and manage multiple ML models using AWS SageMaker
- Route inference requests using an A/B testing mechanism
- Automate infrastructure and deployment using AWS CDK
- Collect and analyze feedback to evaluate model performance
- Implement CI/CD best practices using GitHub Actions
- Gradually scale to include training, model versioning, and evaluation

---

## Tech Stack

**Cloud Infrastructure**
- AWS CDK (Python)
- AWS Lambda
- Amazon SageMaker
- Amazon API Gateway
- Amazon Route 53
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch

**CI/CD & DevOps**
- GitHub Actions
- AWS CLI
- CDK Synth/Deploy
- Flake8 + Pytest
- Secrets Management

**Machine Learning**
- HuggingFace Transformers (GPT-2, GPT-Lite)
- PyTorch / Transformers
- Evaluation logging
- A/B testing logic

---

## Project Roadmap

~~### **Phase 0: CI/CD + Local Environment Setup**~~

**Goal**: Set up development and deployment workflows.

- [x]  ~~Create Conda environments yaml files (`cdk-dev`, `ml-dev`)~~
- [x]  ~~Scaffold GitHub Actions CI/CD pipeline for CDK~~
- [x]  ~~Set up CDK project in Python deploy S3 bucket and IAM permissions~~
- [x]  ~~Store AWS credentials in GitHub Secrets~~

**Deliverables**:

- [x]  ~~`.github/workflows/deploy.yml`~~
- [x]  ~~`cdk/` directory with base infra~~
- [x]  ~~GitHub Actions deploying infra stack automatically~~

**Tech stack**:

`AWS CDK (Python)`, `GitHub Actions`, `Conda`, `IAM`, `S3`

---

~~### **Phase 1: Local Model Training + Testing**~~

**Goal**: Fine-tune GPT-2 model locally and validate outputs.

**Steps**:

- [x]  ~~Train DistilGPT-2 on headlines dataset in Jupyter Notebook~~
- [x]  ~~Test model and tune hyperparameters~~
- [x]  ~~Run local predictions to validate quality~~
- [x]  ~~Save model and tokenizer to disk (`.save_pretrained`)~~

**Deliverables**:

- [x]  ~~Jupyter notebook with training + testing code~~
- [x]  ~~`upload_model.py` script to upload artifacts to S3~~
- [x]  ~~Exported artifacts in `models/`~~

**Tech stack**:

`Hugging Face Transformers`, `Jupyter`, `PyTorch`, `S3`, `Boto3`

---

~~### **Phase 2: Inference Deployment in AWS**~~

**Goal**: Deploy the trained model as a **SageMaker Serverless Inference Endpoint**.

**Steps**:

- [x]  ~~Use CDK to create:~~
    - `S3 bucket` for artifacts
    - `IAM role` for SageMaker
    - `CfnModel`, `CfnEndpointConfig`, and `CfnEndpoint`
- [x]  ~~Upload model.tar.gz to S3~~
- [x]  ~~Deploy endpoint via CDK~~
- [x]  ~~Invoke endpoint using `invoke_endpoints.py`~~

**Deliverables**:

- [x]  ~~`inference_stack.py` with SageMaker setup~~
- [x]  ~~Endpoint name stored in SSM~~
- [x]  ~~Successfully invoked endpoint with real output~~

**Tech stack**:

`SageMaker Serverless`, `CDK`, `SSM`, `Boto3`, `IAM`, `S3`

---

### **Phase 3: API Gateway + Lambda + Network Security + Unit Testing**

**Goal**: Expose inference endpoint via HTTP API and add pre-processing logic.

**Steps**:

- [ ]  Add `Lambda function` that:
    - Validates input
    - Sends request to SageMaker
    - Handles errors / warm-up logic
- [ ]  Add `API Gateway` endpoint (public or secured)
- [ ]  Start creating unit + integration tests for Lambda
- [ ]  Add rate limiting / throttling to prevent abuse

**Deliverables**:

- [ ]  `lambda_handler.py`
- [ ]  CDK deployment of API Gateway + Lambda
- [ ]  `tests/` directory with test cases

**Tech stack**:

`API Gateway`, `Lambda`, `Pytest`, `SSM`, `IAM`, `CloudWatch Logs`

---

### **Phase 4: Frontend UI + Route 53 + Hosting**

**Goal**: Build a basic user-facing UI connected to the API.

**Steps**:

- [ ]  Build static HTML + JS frontend (prompt input, response output)
- [ ]  Add upvote/downvote buttons (disabled initially)
- [ ]  Host frontend via S3 static website hosting
- [ ]  Connect domain using Route 53 and SSL via ACM

**Deliverables**:

- [ ]  `frontend/index.html`, `style.css`, `script.js`
- [ ]  Route 53 configuration
- [ ]  CDN (optional: CloudFront for HTTPS)

**Tech stack**:

`S3 static hosting`, `Route 53`, `HTML/JS`, `CloudFront (optional)`

---

### **Phase 5: Feedback System with Aurora**

**Goal**: Store responses + feedback using Aurora Serverless.

**Steps**:

- [ ]  Provision Aurora Serverless v2 with CDK
- [ ]  Add upvote/downvote recording in Lambda
- [ ]  Store: prompt, response, model, feedback, timestamp

**Deliverables**:

- [ ]  Aurora SQL schema + CDK definition
- [ ]  Updated Lambda logic to write to DB
- [ ]  UI integration: thumbs up/down + Ajax POST to API

**Tech stack**:

`Aurora Serverless`, `CDK`, `PostgreSQL or MySQL`, `Lambda`, `S3`

---

### **Phase 6: A/B Testing + CloudWatch Metrics + Model Labels**

**Goal**: Route requests between two models and visualize metrics.

**Steps**:

- [ ]  Deploy GPT-Lite variant alongside GPT-2
- [ ]  Use SageMaker Production Variants for A/B testing
- [ ]  Log model name in responses
- [ ]  Create dashboard for:
    - Feedback per model
    - Latency, error rate, traffic split

**Deliverables**:

- [ ]  CDK A/B config
- [ ]  CloudWatch metrics setup
- [ ]  Dashboard in CloudWatch or QuickSight

**Tech stack**:

`SageMaker production variants`, `CloudWatch`, `Aurora`, `QuickSight (optional)`

---

### **Phase 7: Classifier Integration (BERT or Similar)**

**Goal**: Auto-classify model output (e.g., category: sports, politics...).

**Steps**:

- [ ]  Train lightweight BERT classifier
- [ ]  Deploy it as second SageMaker endpoint
- [ ]  Extend Lambda to:
    - Route output to classifier
    - Store prediction in Aurora
    - Return category to frontend

**Deliverables**:

- [ ]  `bert_classifier/`
- [ ]  Updated Lambda + Aurora schema
- [ ]  Category displayed in UI

**Tech stack**:

`SageMaker`, `Transformers`, `Lambda`, `Aurora`, `JS UI update`

---
