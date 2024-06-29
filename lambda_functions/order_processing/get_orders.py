import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Orders')

    user_id = event['user_id']

    response = table.query(
        KeyConditionExpression='UserID = :user_id',
        ExpressionAttributeValues={
            ':user_id': user_id
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }
