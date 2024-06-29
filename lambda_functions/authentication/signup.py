import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    username = event['username']
    password = event['password']
    email = event['email']

    response = client.sign_up(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        Username=username,
        Password=password,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
        ],
    )

    return {
        'statusCode': 200,
        'body': json.dumps('User signed up successfully')
    }
