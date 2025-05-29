# Storage Classes

This guide demonstrates creating an S3 bucket, uploading an object with different storage classes, and inspecting the storage class metadata via AWS CLI.

---

## Create a bucket

```sh
aws s3 mb s3://class-change-example-001
```

> Creates an S3 bucket named `class-change-example-001`.

---

## Create a file

```sh
echo "class change" >> myfile.txt
```

> Generates a local text file containing the string "class change".

---

## Upload the file with default storage class (STANDARD)

```sh
aws s3 cp myfile.txt s3://class-change-example-001
aws s3api head-object --bucket class-change-example-001 --key myfile.txt
```

Example output:

```json
{
    "AcceptRanges": "bytes",
    "ContentLength": 13,
    "ETag": "\"dbc3716e480a39040a7f3d324c3f791d\"",
    "ContentType": "text/plain",
    "ServerSideEncryption": "AES256",
    "Metadata": {}
}
```

> **Note:** The `StorageClass` field does not appear if it is the default `STANDARD` storage class.
> For other storage classes, it will be explicitly shown.

---

## Upload the file specifying a different storage class (STANDARD\_IA)

```sh
aws s3 cp myfile.txt s3://class-change-example-001 --storage-class STANDARD_IA
aws s3api head-object --bucket class-change-example-001 --key myfile.txt
```

Example output:

```json
{
    "AcceptRanges": "bytes",
    "LastModified": "2025-05-27T22:02:05+00:00",
    "ContentLength": 13,
    "ETag": "\"dbc3716e480a39040a7f3d324c3f791d\"",
    "ContentType": "text/plain",
    "ServerSideEncryption": "AES256",
    "Metadata": {},
    "StorageClass": "STANDARD_IA"
}
```

---

## 📚 Common S3 Storage Classes

| Storage Class        | Description                                  |
| -------------------- | -------------------------------------------- |
| STANDARD             | Default; frequently accessed data            |
| STANDARD\_IA         | Infrequent Access — lower cost for cold data |
| ONEZONE\_IA          | Infrequent Access stored in a single AZ      |
| INTELLIGENT\_TIERING | Automatically moves data between tiers       |
| GLACIER              | Archive storage; retrieval in minutes/hours  |
| DEEP\_ARCHIVE        | Long-term archive; retrieval takes hours     |

> See the [AWS S3 Storage Classes Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) for details.

---

## Clean up

```sh
aws s3 rm s3://class-change-example-001/myfile.txt
aws s3 rb s3://class-change-example-001
```

> **Important:** Ensure the bucket is empty before deleting it using `rb` (remove bucket).

---

This example clearly shows how to upload objects to S3 with different storage classes, and how to verify the storage class using the `head-object` command. Adjusting storage class helps optimize cost based on access patterns.

---
