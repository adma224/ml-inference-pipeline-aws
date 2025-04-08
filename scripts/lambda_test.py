import lambda_function

event = {"name": "Adrian"}
context = {}  # Can mock more if needed

response = lambda_function.handler(event, context)
print(response)
