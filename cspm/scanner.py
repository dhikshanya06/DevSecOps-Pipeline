import boto3

def check_public_s3_buckets():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets().get('Buckets', [])
    findings = []

    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            for grant in acl['Grants']:
                if grant['Grantee'].get('URI') == "http://acs.amazonaws.com/groups/global/AllUsers":
                    findings.append({
                        "resource": bucket_name,
                        "issue": "Public S3 bucket",
                        "severity": "High"
                    })
        except Exception as e:
            continue

    return findings

def main():
    result = check_public_s3_buckets()
    return {
        "s3_public_buckets": result
    }

if __name__ == "__main__":
    print(main())

