# Bucket Policies

This example demonstrates how to use S3 bucket policies to:

- Grant object-level access to a specific IAM user
- Deny access to a specific folder (e.g. `MySecretFolder/`)
- Keep public access completely blocked

---

## 🪣 Create the Bucket

```sh
aws s3 mb s3://bucket-policy-example-001
````

---

## 🔒 Block Public Access

Ensure that public access is disabled for the bucket:

```sh
aws s3api put-public-access-block \
  --bucket bucket-policy-example-001 \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

---

## 👤 Policy: Grant Access to IAM User (Except a Folder)

We'll create a policy that:

* **Allows** object actions (`GetObject`, `PutObject`, `DeleteObject`) to user `aws-examples-restricted`
* **Denies** access to the path `MySecretFolder/*` within the bucket

### `bucket-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRestrictedUserFullAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/aws-examples-restricted"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::bucket-policy-example-001/*"
    },
    {
      "Sid": "DenyRestrictedUserSecretFolder",
      "Effect": "Deny",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/aws-examples-restricted"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::bucket-policy-example-001/MySecretFolder/*"
    }
  ]
}
```

> 📌 Deny always takes precedence over Allow in AWS IAM evaluation logic.

---

## 🚀 Apply the Policy

```sh
aws s3api put-bucket-policy \
  --bucket bucket-policy-example-001 \
  --policy file://bucket-policy.json
```

---

## 📄 Verify Bucket Policy

```sh
aws s3api get-bucket-policy \
  --bucket bucket-policy-example-001 \
  --query Policy \
  --output text | jq .
```
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowRestrictedUserFullAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/aws-examples-restricted"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::bucket-policy-example-001/*"
    },
    {
      "Sid": "DenyRestrictedUserSecretFolder",
      "Effect": "Deny",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:user/aws-examples-restricted"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::bucket-policy-example-001/MySecretFolder/*"
    }
  ]
}
```
---

## 🧼 Clean Up

```sh
aws s3 rb s3://bucket-policy-example-001 --force
```

---

## 📚 References

* [S3 Bucket Policy Examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
* [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
* [IAM Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
