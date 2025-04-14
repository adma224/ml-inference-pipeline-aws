# Serverless Model Inference Pipeline with AWS CDK & CI/CD

## Project Description

[AWS Infrastructure Diagram](https://github.com/adma224/ml-inference-pipeline-aws/blob/main/diagrams/infrastructure_diagram_aws_ml_pipeline.png) - [Project Roadmap (Currently on Phase 4)](https://github.com/adma224/ml-inference-pipeline-aws/wiki/Project-Roadmap)

This project demonstrates a scalable, production-style inference pipeline using AWS CDK, Lambda, API Gateway, and SageMaker. It includes a fully automated CI/CD pipeline powered by GitHub Actions and is designed to showcase mid-level skills in AWS Cloud Engineering, DevOps, Machine Learning Engineering, and MLOps.

## News Headline Generator – GPT-2 Headline Completion Web App

This web app generates full news headlines based on a few typed words using a fine-tuned GPT-2 model. It's powered entirely by a serverless AWS backend and showcases A/B inference routing, metadata tracking, and CI/CD automation.

The demo is still a work in progress — outputs may be quirky or surprising, but that’s part of the fun as the model improves!

## [Click for live demo here!](https://frontendstack-frontendbucketefe2e19c-uod6vgeirydc.s3.us-east-1.amazonaws.com/index.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIA5OWK4APTVUWQOXME%2F20250410%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250410T202354Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDUaCXVzLWVhc3QtMSJIMEYCIQDZVqyfNoENDvbTFAgRxOoqKi2IKS%2BQ0Q8gDjpGWuDoGwIhAO43bmHAElrJjQNqNoCT%2Bkvcxqj4HXo08ZHsolYYNJqHKuMCCK7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMOTI0OTE3MTcxMTc1IgyR4MeJMgSO3hFQzfUqtwKdW68gFOo8wQpypL%2FzOd0RJn1fYJo8kkQ7JLOVJr%2FrzzTz5IcnI9fr8INCcnr72E7wr4pxje80RjrmSZg7MmbIH%2Fms68qGre%2Bs14EbB%2B8RONS4PWAyQLp3hkuqIJbPEN1IKEMFuJKxsWFo0Sz%2FbbKz0CWj0gHS%2BoX%2Bjlvzwyn0AnYjg3ZpuAiJ2vzhRady%2Fu61oOfjYqPyw3oOgqhpErD815DfZj0MCT4c9EjJN4KWjOBinZoWLU53%2FaOVyfXdX2TpD49ZDSQ9%2FmftHps%2Fxj0mVNQIIxl199nBhyjWdpemSZGNUFHY7piYvS0VDHHhfNeBwPdNjHpPIiUwQpmLtdYiV0tqiI77%2FOIDREJKodwi%2BviVltVE%2FnXb9BkQJvI%2Bnmx7S9DKVjgbKD5BiYWj4sfKe12zy9jDPDC%2F0eC%2FBjqsApyzEwwzHMwvBs4BfaXAXEKSe0p4%2BzEO7WmsckmxYa6Cz9iA3Pme86hirtLbWy80q6%2BIEm1UJGEI4yHJ3xJpBwiDnYnEDMlT3eVyeMwpLOLAMWMT91RWQc8HrrO5WYsejKZiNh9raq7zrxOr4gSzC8dLZEmqrPLatj6IXnuKwgME29FdyYIPzcRVEo8TINIEl6Igm9XP96K8ovEGhfnw5RySisq7A2N4dVOCEv1CcDS%2Fn5im3ppUIB9BqZ4D2U2buwtM78b3zuT%2BQDa%2B5PiI%2FIqyWXqXSVsWfgYwZmlt%2BvbH3IA5vu5CSzW68mQqfcl3xxB1ABFVtOkAXI2pAKLQCRCayLI5T0VGtCB7fc5LXEr9A9O3tGqgVCKuU2pwBWaCxR1T8C%2FSzv4LYQm4Gg%3D%3D&X-Amz-Signature=a926066e259d26420a60faf1e641e4780366329050f21f81115dda2cf574de53&X-Amz-SignedHeaders=host&response-content-disposition=inline)

*Allow 5–15 seconds for the model to warm up after clicking “Generate.” A warm-up mechanism is coming soon.*

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

