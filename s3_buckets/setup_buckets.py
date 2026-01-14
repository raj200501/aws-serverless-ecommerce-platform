"""Local bucket setup for product image storage."""

from pathlib import Path


def create_bucket(bucket_name: str) -> Path:
    root = Path("data") / "s3_buckets"
    root.mkdir(parents=True, exist_ok=True)
    bucket_path = root / bucket_name
    bucket_path.mkdir(exist_ok=True)
    return bucket_path


if __name__ == "__main__":
    bucket = create_bucket("ecommerce-product-images")
    print(f"Local bucket created at {bucket}")
