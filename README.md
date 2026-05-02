# AWS Cost Optimization using Lambda 🚀

Automating AWS cost optimization by cleaning up unused EBS snapshots using serverless architecture.

## 📌 Overview
This project demonstrates how to reduce AWS costs by automatically identifying and deleting stale EBS snapshots using AWS Lambda.

## ❗ Problem
Unused EBS snapshots continue to incur storage costs even after associated EC2 instances or volumes are deleted.

## 💡 Solution
A serverless AWS Lambda function written in Python (Boto3) that:
- Identifies stale snapshots
- Deletes unused snapshots automatically

## ⚙️ How It Works
1. Fetch all snapshots
2. Check associated volumes
3. Verify attachment to EC2 instances
4. Delete snapshots older than 30 days

## 🔐 IAM Permissions Required
- ec2:DescribeSnapshots
- ec2:DeleteSnapshot
- ec2:DescribeVolumes
- ec2:DescribeInstances

## 🚀 Future Scope
- Add SNS alerts before deletion
- Implement tag-based filtering

## 👨‍💻 Author
Kunja Ravikiran
