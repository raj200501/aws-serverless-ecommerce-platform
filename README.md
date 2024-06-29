# Serverless E-Commerce Platform

This repository contains the code for a serverless e-commerce platform built using AWS services. The platform includes user authentication, product management, order processing, and a recommendation system.

## Features

- User Authentication (AWS Cognito)
- Product Management (AWS Lambda, API Gateway, DynamoDB)
- Order Processing (AWS Lambda, API Gateway, DynamoDB)
- Recommendation System (AWS Lambda, S3)
- Infrastructure as Code (Serverless Framework)

## Getting Started

### Prerequisites

- Node.js
- Serverless Framework
- AWS CLI

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/serverless-ecommerce-platform.git
    cd serverless-ecommerce-platform
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Deploy the infrastructure:
    ```bash
    serverless deploy
    ```

4. Set up DynamoDB tables and Cognito user pool:
    ```bash
    python backend/dynamodb/setup_tables.py
    python backend/cognito/setup_cognito.py
    ```

## License

This project is licensed under the MIT License.
