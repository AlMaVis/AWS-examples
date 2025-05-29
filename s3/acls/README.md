# ACLs

This repository contains practical commands and examples illustrating the use of AWS S3 Access Control Lists (ACLs) and related bucket configurations. These snippets reflect real-world usage with `awscli` (`s3api`), supporting an understanding of S3 access management relevant to the AWS Solutions Architect Associate certification.

---

## Create a new bucket

```sh
aws s3api create-bucket --bucket acl-example-001 --region us-east-1
```

> Creates an S3 bucket named `acl-example-001` in the `us-east-1` region using the low-level `s3api` command for full control over API parameters.
> [AWS CLI Docs: create-bucket](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/create-bucket.html)

---

## Turn off Block Public Access for ACLs

```sh
aws s3api put-public-access-block \
--bucket acl-example-001 \
--public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,RestrictPublicBuckets=true,BlockPublicPolicy=true"
```

> Modifies the Public Access Block settings to allow ACL-based public access while restricting public bucket policies.
> This is important to enable ACLs to function without being blocked by global bucket settings.
> [AWS CLI Docs: put-public-access-block](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/put-public-access-block.html)
> [AWS Docs: S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html)

---

## Show Public Access Block configuration

```sh
aws s3api get-public-access-block --bucket acl-example-001
```

```json
{
  "PublicAccessBlockConfiguration": {
    "BlockPublicAcls": false,
    "IgnorePublicAcls": false,
    "BlockPublicPolicy": true,
    "RestrictPublicBuckets": true
  }
}
```

> Retrieves current public access block settings on the bucket to verify ACL and policy restrictions.

---

## Change Bucket Ownership Controls

```sh
aws s3api put-bucket-ownership-controls \
--bucket acl-example-001 \
--ownership-controls "Rules=[{ObjectOwnership=BucketOwnerPreferred}]"
```

> Applies ownership control settings so that objects uploaded by other AWS accounts are automatically owned by the bucket owner, simplifying access management.
> [AWS CLI Docs: put-bucket-ownership-controls](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/put-bucket-ownership-controls.html)
> [AWS Docs: Object Ownership](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html)

---

## Show Ownership Controls

```sh
aws s3api get-bucket-ownership-controls --bucket acl-example-001
```

```json
{
  "OwnershipControls": {
    "Rules": [
      {
        "ObjectOwnership": "BucketOwnerPreferred"
      }
    ]
  }
}
```

> Confirms the applied ownership controls on the bucket.

---

## Change ACLs to allow a user in another AWS Account

```sh
aws s3api put-bucket-acl \
  --bucket acl-example-001 \
  --access-control-policy file://acl-policy.json
```

> Updates the bucket ACL using a JSON file (`acl-policy.json`) that defines grants for external AWS accounts or users.
> This is essential for cross-account access using ACLs.
> [AWS CLI Docs: put-bucket-acl](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/put-bucket-acl.html)
> [AWS Docs: Using ACLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html)

---

## Show the Modified Bucket ACL

```sh
aws s3api get-bucket-acl --bucket acl-example-001
```

```json
{
  "Grants": [
    {
      "Grantee": {
        "ID": "*** Grantee-Canonical-User-ID ***",
        "Type": "CanonicalUser"
      },
      "Permission": "FULL_CONTROL"
    }
  ],
  "Owner": {
    "ID": "*** Owner-Canonical-User-ID ***"
  }
}
```

> Displays the current ACL settings on the bucket, showing all grants including external users with their permissions.
> The canonical user IDs uniquely identify AWS accounts/users.

---

## Clean Up
```sh
aws s3 rb s3://acl-example-001
```

### Additional Resources

* [AWS CLI Reference: s3api](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/index.html)
* [Amazon S3 ACL Concepts](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html)
* [AWS Solutions Architect Associate Exam Guide](https://aws.amazon.com/certification/certified-solutions-architect-associate/)

