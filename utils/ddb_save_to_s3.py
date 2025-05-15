import argparse
import json
import boto3
from botocore.exceptions import ClientError

def export_table_to_s3(source_table_name, bucket_name, object_key, region='us-east-1'):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    source_table = dynamodb.Table(source_table_name)
    s3 = boto3.client('s3')

    print(f"Scanning source table: {source_table_name}")
    response = source_table.scan()
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = source_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    print(f"Total items to migrate: {len(items)}")

    # Convert to JSON and write to S3
    json_data = json.dumps(items, indent=2, default=str)
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=json_data.encode('utf-8'))

    print(f"Exported {len(items)} items to s3://{bucket_name}/{object_key}")

def main():
    # Usage
    # export_table_to_s3("OldTableName", "your-s3-bucket", "dynamodb/backup.json")
    export_table_to_s3("PRReviews", "codeominous-s3-bucket", "dynamodb/prreviews/backup.json", "us-east-1")

if __name__ == '__main__':
    main()
