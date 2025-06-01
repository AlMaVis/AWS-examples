# S3 Client-Side Encryption Hands-On Reference

This document summarizes a hands-on experience with client-side encryption for Amazon S3 using a raw AES-256 key and the AWS Encryption SDK for Python. The steps and commands are collected as a reference for future AWS projects and AWS Solutions Architect certification preparation. For detailed explanations, refer to the official AWS documentation linked below.

---

## Key Generation and Usage

- **Generate a 256-bit (32 bytes) random key and encode it in base64:**  
  ```sh
  openssl rand -base64 32 > raw.key.b64
  ```

- **Use the key with the Python script:**  
  ```sh
  python encrypt.py upload --raw-key-b64 "$(cat raw.key.b64)"
  python encrypt.py download --raw-key-b64 "$(cat raw.key.b64)"
  ```

---

## encrypt.py Overview

The `encrypt.py` script demonstrates client-side encryption and decryption using a raw AES-256 keyring with the [AWS Encryption SDK for Python](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html).  
- **Upload mode:** Encrypts the example data (`Hello World`) using the provided AES key and uploads the ciphertext to the S3 bucket `encryption-client-side-example-001` with the key `myfile.txt`.
- **Download mode:** Downloads the ciphertext from S3, decrypts it using the same AES key, and prints the plaintext to the console.

**Key points:**
- Uses a raw AES-256 key (not KMS).
- Demonstrates both encryption/upload and download/decryption.
- Encryption context is included for demonstration.

---

## Example Usage

- **Encrypt and upload:**
  ```sh
  python encrypt.py upload --raw-key-b64 "$(cat raw.key.b64)"
  ```

- **Download and decrypt:**
  ```sh
  python encrypt.py download --raw-key-b64 "$(cat raw.key.b64)"
  ```

---

## Clean Up

```sh
aws s3 rb s3://encryption-client-side-example-001 --force
```

## References

- [AWS Encryption SDK for Python](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html)
- [Raw AES Keyring (AWS Encryption SDK)](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/keyrings.html#keyrings-raw-aes)
- [Amazon S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [AWS CLI S3 Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html)