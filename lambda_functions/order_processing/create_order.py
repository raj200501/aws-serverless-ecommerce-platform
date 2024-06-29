import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Orders')

    order_id = event['order_id']
    user_id = event['user_id']
    product_ids = event['product_ids']
    total_price = event['total_price']

    table.put_item(
        Item={
            'OrderID': order_id,
            'UserID': user_id,
            'ProductIDs': product_ids,
            'TotalPrice': total_price,
            'CreatedAt': datetime.utcnow().isoformat()
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Order created successfully')
    }
