import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Products')

    user_id = event['user_id']

    # Mock recommendation logic
    response = table.scan()
    recommendations = response['Items'][:5]

    return {
        'statusCode': 200,
        'body': json.dumps(recommendations)
    }
