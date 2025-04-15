import boto3
import os

rds = boto3.client("rds-data")

def handler(event, context):
    sql = """
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        vote TEXT,
        model TEXT,
        prompt TEXT,
        response TEXT,
        timestamp TIMESTAMPTZ DEFAULT now()
    );
    """

    try:
        response = rds.execute_statement(
            secretArn=os.environ["DB_SECRET_ARN"],
            resourceArn=os.environ["CLUSTER_ARN"],
            database=os.environ["DB_NAME"],
            sql=sql
        )

        print("Table creation result:", response)
        return {
            "Status": "SUCCESS",
            "Message": "feedback table created or already exists"
        }

    except Exception as e:
        print("Error creating table:", str(e))
        return {
            "Status": "FAILED",
            "Reason": str(e)
        }
