import boto3
import json
import sys

# Usage:
#   python update_ab_weights.py gpt2-endpoint 0.9 0.1
# meaning 90% -> VariantA, 10% -> VariantB

endpoint_name = sys.argv[1] if len(sys.argv) > 1 else "gpt2-endpoint"
a_weight = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
b_weight = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0

sm = boto3.client("sagemaker")

resp = sm.update_endpoint_weights_and_capacities(
    EndpointName=endpoint_name,
    DesiredWeightsAndCapacities=[
        {"VariantName": "VariantA", "DesiredWeight": a_weight},
        {"VariantName": "VariantB", "DesiredWeight": b_weight},
    ],
)

print("Update initiated:")
print(json.dumps(resp, default=str, indent=2))
