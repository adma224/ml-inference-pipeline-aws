# :poodle: Model Inference Pipeline with AWS CDK and CI/CD

This project demonstrates a scalable, production-style inference pipeline using AWS CDK, Lambda, API Gateway, and SageMaker. It includes a fully automated CI/CD pipeline powered by GitHub Actions and is designed to showcase mid-level skills in AWS Cloud Engineering, DevOps, Machine Learning Engineering, and MLOps.

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

## ✅ Phase 0: CI/CD & Environment Setup

- Set up GitHub Actions for continuous deployment.
- Defined Conda environment for local reproducibility.
- Deployed CDK infrastructure with a multi-stack architecture.
- Bootstrapped the AWS environment for asset publishing.

---

## ✅ Phase 1: Model Training & Packaging

- Fine-tuned a DistilGPT-2 model using Hugging Face + PyTorch.
- Exported model artifacts and tokenizer to `model.tar.gz` and `tokenizer.tar.gz`.
- Stored artifacts in a versioned S3 bucket for reproducible inference.
- Prepared assets for deployment in SageMaker Serverless.

---

## ✅ Phase 2: Serverless Model Inference Deployment

- Deployed the trained model to a SageMaker Serverless Inference endpoint.
- Used a prebuilt Hugging Face inference container.
- Stored the endpoint name in AWS SSM for decoupled access.
- Verified functionality with an invoke script and test prompt.

---

## ✅ Phase 3: Lambda Gateway Integration

- Built a Lambda function that acts as a secure proxy to the inference endpoint.
- Added warm-up logic to minimize latency for first-time requests.
- Performed basic error handling and input validation.
- Connected Lambda to API Gateway for scalable HTTPS access.

---

📌 *Next Phases will include model registry, canary deployments, user feedback tracking, and real-time A/B testing.*
