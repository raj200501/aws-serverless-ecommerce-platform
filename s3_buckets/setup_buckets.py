import boto3

def create_bucket(bucket_name):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)

if __name__ == '__main__':
    create_bucket('ecommerce-product-images')
    print("S3 bucket created successfully")
