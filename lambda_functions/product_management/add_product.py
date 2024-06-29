import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Products')

    product_id = event['product_id']
    name = event['name']
    price = event['price']
    category = event['category']

    table.put_item(
        Item={
            'ProductID': product_id,
            'Name': name,
            'Price': price,
            'Category': category,
            'CreatedAt': datetime.utcnow().isoformat()
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Product added successfully')
    }
