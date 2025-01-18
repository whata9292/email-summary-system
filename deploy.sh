#!/bin/bash

# 変数設定
STACK_NAME="email-summary-stack"
ENVIRONMENT="dev"

# CloudFormationスタックのデプロイ
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name $STACK_NAME \
  --parameter-overrides \
    Environment=$ENVIRONMENT \
  --capabilities CAPABILITY_IAM

# デプロイ後のECRリポジトリURIの取得
ECR_REPO_URI=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].Outputs[?OutputKey==`ECRRepositoryUri`].OutputValue' \
  --output text)

# ECRへのログイン
aws ecr get-login-password --region ap-northeast-1 | \
  docker login --username AWS --password-stdin $ECR_REPO_URI

# Dockerイメージのビルドとプッシュ
docker build -t email-summary .
docker tag email-summary:latest $ECR_REPO_URI:latest
docker push $ECR_REPO_URI:latest