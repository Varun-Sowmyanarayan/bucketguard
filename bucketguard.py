import boto3
from moto import mock_aws

REGION = "us-east-1"

BUCKETS = ["bg-safe-one", "bg-safe-two", "bg-risky-one", "bg-risky-two"]


def create_buckets(s3):
    for name in BUCKETS:
        s3.create_bucket(Bucket=name)
        print("Created bucket:", name)


def make_safe(s3, name):
    # Block all public access
    s3.put_public_access_block(
        Bucket=name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )
    # Turn on encryption
    s3.put_bucket_encryption(
        Bucket=name,
        ServerSideEncryptionConfiguration={
            "Rules": [
                {"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
            ]
        },
    )
    # Turn on versioning
    s3.put_bucket_versioning(
        Bucket=name,
        VersioningConfiguration={"Status": "Enabled"},
    )


def make_risky(s3, name):
    # Make the bucket publicly readable (a classic mistake)
    s3.put_bucket_acl(Bucket=name, ACL="public-read")


def check_public_access(s3, name):
    # PASS only if all four "block public access" switches are on
    try:
        config = s3.get_public_access_block(Bucket=name)
        settings = config["PublicAccessBlockConfiguration"]
        return all(settings.values())
    except Exception:
        # No block configured at all means the bucket is not protected
        return False


def check_encryption(s3,name):
    try:
        s3.get_bucket_encryption(Bucket=name)
        return True
    except Exception:
        return False

def check_versioning(s3,name):
    response=s3.get_bucket_versioning(Bucket=name)
    return response.get("Status") == "Enabled"


def audit_bucket(s3, name):
    results = {
        "Public access blocked": check_public_access(s3, name),
        "Encryption on": check_encryption(s3, name),
        "Versioning on": check_versioning(s3, name),
    }
    print("\nBucket:", name)
    for check, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print("  ", check, "->", status)
    overall = "PASS" if all(results.values()) else "FAIL"
    print("   OVERALL ->", overall)

def main():
    with mock_aws():
        s3=boto3.client("s3", region_name=REGION)
        create_buckets(s3)

        for name in BUCKETS:
            if "safe" in name:
                make_safe(s3,name)
            else:
                make_risky(s3,name)
        print("\n==== BUCKETGUARD REPORT ====")
        for name in BUCKETS:
            audit_bucket(s3,name)
if __name__ == "__main__":
    main()
    

