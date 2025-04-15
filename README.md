# AWS Serverless Generative ML Microservices Infra with CloudFormation & CI/CD

## Project Description

[AWS Infrastructure Diagram](https://github.com/adma224/ml-inference-pipeline-aws/blob/main/diagrams/infrastructure_diagram_aws_ml_pipeline.png) - [Project Roadmap (Currently on Phase 4)](https://github.com/adma224/ml-inference-pipeline-aws/wiki/Project-Roadmap)

This project showcases an advanced, production-style ML inference pipeline built on AWS using SageMaker, Lambda, API Gateway, and CDK. It showcases modern microservices principles by implementing loosely coupled, single-responsibility components deployed serverlessly for scalable, fault-isolated ML serving. Designed for real-world relevance, it includes A/B testing capabilities, model versioning, feedback logging, and model output analytics with plans for visualization. A fully automated CI/CD pipeline powered by GitHub Actions ensures continuous delivery and infrastructure consistency.

More than just infrastructure, this project reflects cutting-edge MLOps practices and hands-on expertise in deploying generative AI workflows (GPT2) with a focus on scalability, modularity, and cost efficiency. 

## News Headline Generator – GPT-2 Headline Completion Web App

This web app generates full news headlines based on a few typed words using a fine-tuned GPT-2 model. It's powered entirely by a serverless AWS backend and showcases A/B inference routing, metadata tracking, and CI/CD automation.

The demo is still a work in progress — outputs may be quirky or surprising!

## [Click for live demo here!](https://frontendstack-frontendbucketefe2e19c-3i0kyc8qz5eb.s3.us-east-1.amazonaws.com/index.html)

### How to Use

1. Type the beginning of a news headline
2. Click **Generate**
3. Receive a completed headline based on your input

#### Example Prompts
- `Scientists discover`
- `New law passed to`
- `AI could soon`
- `Stock market reacts`
---







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

