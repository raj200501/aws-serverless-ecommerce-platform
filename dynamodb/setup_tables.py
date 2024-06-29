import boto3

def create_products_table():
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
        TableName='Products',
        KeySchema=[
            {
                'AttributeName': 'ProductID',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ProductID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table

def create_orders_table():
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.create_table(
        TableName='Orders',
        KeySchema=[
            {
                'AttributeName': 'OrderID',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'UserID',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'OrderID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'UserID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table

if __name__ == '__main__':
    products_table = create_products_table()
    print("Products table created successfully")

    orders_table = create_orders_table()
    print("Orders table created successfully")
