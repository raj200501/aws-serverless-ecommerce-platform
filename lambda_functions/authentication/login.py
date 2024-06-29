import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    username = event['username']
    password = event['password']

    response = client.initiate_auth(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password,
        },
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response['AuthenticationResult'])
    }
