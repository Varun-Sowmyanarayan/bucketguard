# BucketGuard: The S3 public access auditor
This is a small cloud security proejct that audits S3 buckets for common misconfigurations.

##Here is what it does

Creates 4 fake S3 buckets: 2 secure and 2 deliberately misconfigured

Checks each bucket for:
Public access blocked
Encryption on
Versioning on
Prints a PASS or FAIL result per check and an overall result per bucket.

And then it saves the report to the "report.txt"

##Here is how to run it
```bash
python3 -m venv venv
source venv/bin/activate
pip install boto3 "moto[s3]"
chmod +x run.sh
./run.sh
```

#tech stack used

Python, boto3, moto, Bash

##This is what I learned:

how s3 public access blocks, encryption and versioning work
how to test aws code safely with a mock, with no cost
how to automate a run with a bash script

