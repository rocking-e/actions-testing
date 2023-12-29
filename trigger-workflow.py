#!/usr/bin/env python3
"""
A script to trigger a GitHub Actions workflow
"""
import json
import os
import requests
import sys

github = "api.github.com"
repo = "actions-testing"
owner = "rocking-e"
workflow_name = "Lambda Responder"
token = os.getenv("GIT_TOKEN")
base_url = f"https://{github}/repos/{owner}/{repo}"

payload = {"region": "us-west-2", "amiVersion": "2023.09.27.21", "os": "Amazon Linux 2", "operation": "Add", "amiName": "fix-gha-username-jc-os-arm64-20230927-2125", "amiId": "ami-0234eb653a61a925e", "accounts": ["441554336244", "884947639603", "512445113664"], "tags": [{"Key": "Brand", "Value": "Expedia Product & Technology"}, {"Key": "IMF_Design_Name", "Value": "jc-os"}, {"Key": "Name", "Value": "fix-gha-username-jc-os-arm64-20230927-2125"}, {"Key": "Release", "Value": "20230927-2125"}, {"Key": "Team", "Value": "HICore-Virtualization"}, {"Key": "CPU_Architecture", "Value": "arm64"}, {"Key": "CostCenter", "Value": "95123"}, {"Key": "Base_AMI_Name", "Value": "amzn2-ami-hvm-2.0.20230912.0-arm64-gp2"}, {"Key": "OS_Version", "Value": "Amazon Linux 2"}, {"Key": "Application", "Value": "image-factory-goldenami"}, {"Key": "Base_AMI_Id", "Value": "ami-0234eb653a61a925e"}], "transaction_guid": "c35e6e15-3583-4586-a46b-90c58cc9ce78", "call_guid": "2335e5b2-da54-4bc5-aa94-92a52bf42021", "activity_guid": "78c5e7f2-3dec-47f6-b9d5-3416c06aad8a", "lambda_request_id": "09d545e3-868d-41c4-81d4-8cf52b93ac79", "log_group_name": "/aws/lambda/tf-golden-ami-register-service-prod", "log_stream_name": "2023/09/27/[$LATEST]5c82e394d53f4be5bf1c4a9dfc38978b", "regionToAmiMapping": {"eu-west-1": "ami-01b90d18106de531f", "ap-northeast-2": "ami-0e2e5310e41101ebc", "ap-northeast-1": "ami-0a485d1f60a26525f", "sa-east-1": "ami-0fcd4abd669fffb0f", "ap-southeast-1": "ami-0ded0399569d7dac5", "us-east-1": "ami-0624f9d88ff3b7902", "us-east-2": "ami-00b0c1513c260255a", "us-west-1": "ami-03ac3a54b1bb97d3b", "us-west-2": "ami-08b7d257203a2b8ff"}, "createdDate": "2023-09-27T22:01:59", "status": "ACTIVE"}

authorization = f"Bearer {token}"
headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-ApiVersion": "2022-11-28",
    "Authorization": authorization,
}

# Search workflows to find workflow_id for specified workflow
url_list_workflow_dispatch = f"{base_url}/actions/workflows?per_page=100"
r = requests.get(
    url=url_list_workflow_dispatch,
    headers=headers
)
workflow_id = None
if r.status_code == 200:
    for workflow in r.json().get("workflows"):
        name = workflow.get("name")
        id = workflow.get("id")
        if workflow_name == name:
            workflow_id = id
            print(f"Found {workflow_name}, id = {workflow_id}")

if workflow_id is None:
    print(f"Could not find workflow named {workflow_name}")
    sys.exit(9)

data = {}
data["ref"] = "main"
data["inputs"] = {"design": "from_script", "payload": json.dumps(payload)}
json_data = json.dumps(data)

url_workflow_dispatch = f"{base_url}/actions/workflows/{workflow_id}/dispatches"
r = requests.post(
    url = url_workflow_dispatch,
    data = json_data,
    headers = headers,
)

print(r)
print(f"status code = {r.status_code}")
