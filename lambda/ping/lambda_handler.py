# ../lambda/ping/lambda_function.py
def handler(event, context):
    return {
        "statusCode": 200,
        "body": "pong"
    }
