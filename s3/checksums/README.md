## Create a new se bucket

```sh
aws s3 mb s3://checksums-examples-00012
```

## Create a file that will we do a checksum on

```sh
echo "checksum" > myfile.txt
```

## Get a checksum of a file for md5
```sh
md5sum myfile.txt
```
```sh
bd4a9b642562547754086de2dab26b7d  myfile.txt
```


## Upload our file to s3
```sh
aws s3 cp myfile.txt s3://checksums-examples-00012
aws s3api head-object --bucket checksums-examples-00012 --key myfile.txt
```
```sh
{
    "AcceptRanges": "bytes",
    "ContentLength": 9,
    "ETag": "\"bd4a9b642562547754086de2dab26b7d\"",
    "ContentType": "text/plain",
    "ServerSideEncryption": "AES256",
    "Metadata": {}
}
```

## Upload a file with different checksum
```sh
openssl dgst -sha1 -binary myfile.txt | base64
```
```sh
Ll2vAgHd6waKYtXgjaGGV6ssa+k=  myfile.txt
```

```sh
aws s3api put-object \
  --bucket checksums-examples-00012 \
  --key myfilesha1.txt \
  --body myfile.txt \
  --checksum-algorithm SHA1 \
  --checksum-sha1 Ll2vAgHd6waKYtXgjaGGV6ssa+k=
```
```sh
{
    "ETag": "\"bd4a9b642562547754086de2dab26b7d\"",
    "ChecksumSHA1": "Ll2vAgHd6waKYtXgjaGGV6ssa+k=",
    "ChecksumType": "FULL_OBJECT",
    "ServerSideEncryption": "AES256"
}
```

## Remove all objects and the bucket
``sh
aws s3 rm "s3://checksums-examples-00012/" --recursive --output text
aws s3api delete-bucket --bucket checksums-examples-00012
``