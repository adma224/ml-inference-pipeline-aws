# :poodle: Serverless Model Inference Pipeline with AWS CDK & CI/CD

#### News Headline Generator – GPT-2 Headline Completion Web App

This web app generates full news headlines based on a few typed words using a fine-tuned GPT-2 model. It's powered entirely by a serverless AWS backend and showcases A/B inference routing, metadata tracking, and CI/CD automation.

The demo is still a work in progress — outputs may be quirky or surprising, but that’s part of the fun as the model improves!


## [Click for live demo here!](https://frontendstack-frontendbucketefe2e19c-uod6vgeirydc.s3.us-east-1.amazonaws.com/index.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIA5OWK4APTROBDYOXO%2F20250410%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250410T052833Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECYaCXVzLWVhc3QtMSJIMEYCIQD9rjDN1e3mCv%2BE2AOG%2BHRg1Hzdp%2FRNebVXMXIfcEk4ZwIhAKKpTB7JNnrjhWG%2BvZKaxip0vRqHRRnZ%2FVAlErZCARdnKuMCCJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMOTI0OTE3MTcxMTc1IgzvczDhrHWAMVoW%2BHwqtwIvDDhF7kdsPyPEpX93r9B9spAY2pSzBvRY0cwLwz9vVmPTkNKCBCpqd3aA98OhtPSWlCP4otZKGvYNieZyB2gCf9rlWELjC5tmjiKNqK9rQTkDqu3JoW2X6WjjVEyhKTcCh2XkOYQ6CsaChylb2kt69WqJXvC8PfM5Z9wtfOD%2FuKFOOAMWyStCUj%2FWprg6CQLaaZyaa2QHOnW2kVob%2FkmJXxMYmal3091YJTPQKN0ObrZAXwROwkot7KzXXhcOzc2jBzVDpcqwBJgFk1dZkyjVfvbZQKOn0Xjglhevvyi%2B%2BiBUVYOmA1t0CYlwX1KR9mkY7BcKXWn6aSVPfk5YT404IiYLDK1vkRuzCjok2kx5Iw8ghgnkyRkjQvKy5Zv6IOLCD1a%2Bua2nWyGgxt%2FGIb318Q4U5jlZ9TDord2%2FBjqsAtjORp2cnF7eD%2BL2jSDEoixCCyg9hrB5LvJc2hfRa7nQVigS5ylUFp%2B0lD%2Fr%2B2eshsPx38hhd1Xi3OAjUs%2FkoKFYA0Cx6U5KP%2BDFm7zPrKnWBKf1%2FeDS3mYlXF%2BF9R6ofC8OZ1utCn5fVgNcKX79gqMW%2FRgMOwQbOTHisTCF2tTK8qUQNvmd1w2UYupeycKFpdvMYircZV%2B2JaHsrHAokVjTF7tvh7iKxewlJHYbrt1HCegPaN5q95e%2FZZUZSXspDTmS2ktMxVMnX8pvTEr%2FJRtFcmWShcXRhcz3V2L7egulbR3q8SZ%2Fr7F0dd4kmNhf%2F2rbe8HpyYr53PQ8VL20nyaxXQlZHxUXcLQufx83kpPlCWdPZ6Zw0AdaguQSq0HXDi%2FYwgmycT%2F2DnYyvw%3D%3D&X-Amz-Signature=cfd03c112d6d8b5e66e35d4d0d6d03a8f0335f1f78ad88eb92e1d592f7d81ca1&X-Amz-SignedHeaders=host&response-content-disposition=inline)

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

## Project Description

This project demonstrates a scalable, production-style inference pipeline using AWS CDK, Lambda, API Gateway, and SageMaker. It includes a fully automated CI/CD pipeline powered by GitHub Actions and is designed to showcase mid-level skills in AWS Cloud Engineering, DevOps, Machine Learning Engineering, and MLOps.


[AWS Infrastructure Diagram](https://github.com/adma224/ml-inference-pipeline-aws/blob/main/diagrams/infrastructure_diagram_aws_ml_pipeline.png) - [Project Roadmap (Currently on Phase 4)](https://github.com/adma224/ml-inference-pipeline-aws/wiki/Project-Roadmap)


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

