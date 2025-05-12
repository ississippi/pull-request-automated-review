import argparse
import boto3
from botocore.exceptions import ClientError

def migrate(source_table_name, target_table_name, region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    source_table = dynamodb.Table(source_table_name)
    target_table = dynamodb.Table(target_table_name)

    print(f"Scanning source table: {source_table_name}")
    response = source_table.scan()
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = source_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    print(f"Total items to migrate: {len(items)}")

    migrated_count = 0

    for item in items:
        try:
            # Put item into target table
            target_table.put_item(Item=item)

            # Delete item from source table using primary key
            key = { 'prId': item['prId'] }  # Add sort key here if needed, e.g., 'sk': item['sk']
            source_table.delete_item(Key=key)

            migrated_count += 1
            if migrated_count % 25 == 0:
                print(f"Migrated and deleted {migrated_count} items...")

        except ClientError as e:
            print(f"Failed on item {item.get('prId', '[no id]')}: {e}")

    print(f"Migration and deletion complete. {migrated_count} items processed.")

def main():
    parser = argparse.ArgumentParser(description='Migrate and delete items between DynamoDB tables.')
    parser.add_argument('--source', required=True, help='Source DynamoDB table name')
    parser.add_argument('--target', required=True, help='Target DynamoDB table name')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')

    args = parser.parse_args()
    migrate(args.source, args.target, args.region)

if __name__ == '__main__':
    main()
