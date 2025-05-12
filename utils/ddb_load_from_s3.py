# import_s3_to_dynamodb.py
import boto3
import json
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def load_data_from_s3(bucket_name, object_key, new_table_name):
    table = dynamodb.Table(new_table_name)

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        data = json.loads(response['Body'].read().decode('utf-8'), parse_float=Decimal)
    except ClientError as e:
        print("Failed to retrieve or parse S3 object:", e)
        return

    with table.batch_writer(overwrite_by_pkeys=[]) as batch:
        for item in data:
            batch.put_item(Item=item)

    print(f"Imported {len(data)} items into DynamoDB table: {new_table_name}")

# Usage
# load_data_from_s3("your-s3-bucket", "dynamodb/backup.json", "NewTableName")
load_data_from_s3("codeominous-s3-bucket ", "dynamodb/prreviews/backup.json", "PRReviews")
