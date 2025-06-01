# S3 Encryption Hands-On Reference

This document summarizes hands-on experience with different S3 encryption options, including SSE-S3, SSE-KMS, and SSE-C. The steps and commands are collected as a reference for future AWS projects and for AWS Solutions Architect certification preparation. For detailed explanations, refer to the official AWS documentation linked in each section.

---

## Bucket and File Preparation

- **Bucket creation:**  
  ```sh
  aws s3 mb s3://encryption-examples-001
  ```
  [AWS CLI: aws s3 mb](https://docs.aws.amazon.com/cli/latest/reference/s3/mb.html)

- **Test file creation:**  
  ```sh
  echo "encryption file" >> myfile.txt
  ```

---

## Standard Upload (No Encryption)

- **Put object in bucket:**  
  ```sh
  aws s3 cp myfile.txt s3://encryption-examples-001
  ```
  [Uploading Objects](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html)

---

## Server-Side Encryption with AWS KMS (SSE-KMS)

- **Put object with SSE-KMS:**  
  ```sh
  aws s3api put-object \
    --bucket encryption-examples-001 \
    --key myfile.txt \
    --body myfile.txt \
    --server-side-encryption aws:kms \
    --ssekms-key-id <kms-key-id>
  ```
  [Using SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)

---

## Server-Side Encryption with Customer-Provided Keys (SSE-C)

- **Generate a 256-bit key and related values:**  
  ```sh
  openssl rand -out ssec.key 32
  base64 ssec.key > ssec.key.b64
  openssl md5 -binary ssec.key | base64 > ssec.key.md5
  ```
  [Using SSE-C](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html)

- **Put object with SSE-C:**  
  ```sh
  aws s3api put-object \
    --bucket encryption-examples-001 \
    --key myfile.txt \
    --body myfile.txt \
    --sse-customer-algorithm AES256 \
    --sse-customer-key "$(cat ssec.key.b64)" \
    --sse-customer-key-md5 "$(cat ssec.key.md5)"
  ```

---

## Verifying Encryption

- **Check encryption metadata (SSE-C example):**  
  ```sh
  aws s3api head-object \
    --bucket encryption-examples-001 \
    --key myfile.txt \
    --sse-customer-algorithm AES256 \
    --sse-customer-key "$(cat ssec.key.b64)" \
    --sse-customer-key-md5 "$(cat ssec.key.md5)"
  ```
  [Head Object](https://docs.aws.amazon.com/cli/latest/reference/s3api/head-object.html)

  Example output:
  ```json
  {
      "AcceptRanges": "bytes",
      "LastModified": "2025-05-29T10:24:30+00:00",
      "ContentLength": 16,
      "ETag": "\"072e6b241c63c6ed93adb392********\"",
      "ContentType": "binary/octet-stream",
      "Metadata": {},
      "SSECustomerAlgorithm": "AES256",
      "SSECustomerKeyMD5": "teFot4VXcmEq+yjk********"
  }
  ```

---

## Clean Up

```sh
aws s3 rb s3://encryption-examples-001 --force
```

---

## Key Points

- SSE-S3, SSE-KMS, and SSE-C were tested for object encryption.
- SSE-KMS requires a valid KMS key ID.
- SSE-C requires manual key management and passing the key and its MD5 with each request.
- Encryption metadata is only visible when the correct key is provided for SSE-C.

---

## References

- [Amazon S3 Encryption Overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html)
- [Using SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)
- [Using SSE-C](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html)
- [AWS CLI S3 Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html)