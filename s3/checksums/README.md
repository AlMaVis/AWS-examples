# Checksums

This document demonstrates the use of AWS S3 with checksum operations, showcasing checksum verification during uploads and metadata retrieval using AWS CLI commands. The examples reflect hands-on experience relevant to S3 data integrity concepts tested in the AWS Solutions Architect Associate certification.

---

## Create a new S3 bucket

```sh
aws s3 mb s3://checksums-examples-00012
```

> Creates a new bucket named `checksums-examples-00012` using the higher-level `aws s3` command.
> [AWS CLI Docs: mb (make bucket)](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mb.html)

---

## Create a file to perform checksum on

```sh
echo "checksum" > myfile.txt
```

> Creates a local file `myfile.txt` with the content `"checksum"` for checksum demonstration.

---

## Calculate MD5 checksum of the file

```sh
md5sum myfile.txt
```

```sh
bd4a9b642562547754086de2dab26b7d  myfile.txt
```

> Computes the MD5 checksum locally for verification purposes.
> This checksum is used by S3 as the default `ETag` for single-part uploads without server-side encryption.
> Note: MD5 is not always reliable for multipart uploads or encrypted files.

---

## Upload the file to S3 and verify

```sh
aws s3 cp myfile.txt s3://checksums-examples-00012
aws s3api head-object --bucket checksums-examples-00012 --key myfile.txt
```

```json
{
    "AcceptRanges": "bytes",
    "ContentLength": 9,
    "ETag": "\"bd4a9b642562547754086de2dab26b7d\"",
    "ContentType": "text/plain",
    "ServerSideEncryption": "AES256",
    "Metadata": {}
}
```

> Uploads the file using `aws s3 cp`, a simplified command that handles transfers.
> Then retrieves object metadata with `s3api head-object` showing the `ETag` (MD5 checksum for this object), encryption status, and content length.
> [AWS CLI Docs: s3 cp](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html)
> [AWS CLI Docs: s3api head-object](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/head-object.html)

---

## Calculate SHA1 checksum locally

```sh
openssl dgst -sha1 -binary myfile.txt | base64
```

```sh
Ll2vAgHd6waKYtXgjaGGV6ssa+k=  myfile.txt
```

> Uses OpenSSL to generate a binary SHA1 digest of the file, then encodes it in Base64 format — the format required by S3 for specifying checksums on upload.
> This demonstrates how to prepare checksums other than MD5 for S3's checksum API.

---

## Upload a file with SHA1 checksum validation

```sh
aws s3api put-object \
  --bucket checksums-examples-00012 \
  --key myfilesha1.txt \
  --body myfile.txt \
  --checksum-algorithm SHA1 \
  --checksum-sha1 Ll2vAgHd6waKYtXgjaGGV6ssa+k=
```

```json
{
    "ETag": "\"bd4a9b642562547754086de2dab26b7d\"",
    "ChecksumSHA1": "Ll2vAgHd6waKYtXgjaGGV6ssa+k=",
    "ChecksumType": "FULL_OBJECT",
    "ServerSideEncryption": "AES256"
}
```

> Uploads the file while explicitly specifying the SHA1 checksum, allowing S3 to verify data integrity during the transfer.
> The response confirms the checksum stored alongside the object metadata.
> This feature improves data validation beyond the default MD5 ETag.
> [AWS CLI Docs: put-object with checksum](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/put-object.html)
> [AWS Docs: S3 Checksum Support](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html#API_PutObject_RequestSyntax)

---

## Clean up resources

```sh
aws s3 rm "s3://checksums-examples-00012/" --recursive --output text
aws s3api delete-bucket --bucket checksums-examples-00012
```

> Deletes all objects in the bucket recursively, then deletes the bucket itself to avoid resource sprawl.
> Using `aws s3 rm` for bulk deletion and `s3api delete-bucket` to remove the bucket.
> [AWS CLI Docs: s3 rm](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html)
> [AWS CLI Docs: s3api delete-bucket](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/delete-bucket.html)

---

### Additional Notes

* The default `ETag` returned by S3 is typically the MD5 checksum of the object for simple uploads but can differ for multipart or encrypted uploads.
* Using the `--checksum-algorithm` and checksum parameters in `put-object` commands ensures stronger integrity checks.
* `aws s3api` commands provide granular control and access to advanced S3 features compared to the higher-level `aws s3` commands.
