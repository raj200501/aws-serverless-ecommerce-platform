import boto3

def create_user_pool():
    client = boto3.client('cognito-idp')

    response = client.create_user_pool(
        PoolName='ECommerceUserPool',
        Policies={
            'PasswordPolicy': {
                'MinimumLength': 8,
                'RequireUppercase': True,
                'RequireLowercase': True,
                'RequireNumbers': True,
                'RequireSymbols': False
            }
        },
        AutoVerifiedAttributes=[
            'email'
        ]
    )

    user_pool_id = response['UserPool']['Id']
    return user_pool_id

def create_user_pool_client(user_pool_id):
    client = boto3.client('cognito-idp')

    response = client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName='ECommerceUserPoolClient',
        GenerateSecret=False,
        ExplicitAuthFlows=[
            'ALLOW_USER_PASSWORD_AUTH',
            'ALLOW_REFRESH_TOKEN_AUTH'
        ]
    )

    client_id = response['UserPoolClient']['ClientId']
    return client_id

if __name__ == '__main__':
    user_pool_id = create_user_pool()
    print("User pool created successfully")

    client_id = create_user_pool_client(user_pool_id)
    print("User pool client created successfully")
