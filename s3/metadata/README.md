## Create a bucket

```sh
aws s3 mb s3://metadata-example-001
```

## Create a new file
```sh
echo "metadata" > file.txt
```

## Upload file with metadata
```sh
aws s3api put-object --bucket metadata-example-001 --key file.txt --body file.txt --metadata Meta=Data,Author=Alice,Env=Dev
```

## Get Metadata through head object
```sh
aws s3api head-object --bucket metadata-example-001 --key file.txt
```
Note: Metadata keys are case-insensitive and returned in lowercase.
```sh
{
    "AcceptRanges": "bytes",
    "ContentLength": 9,
    "ETag": "\"b3348b95d7571534c9a0b0fbc28bc5be\"",
    "ContentType": "binary/octet-stream",
    "ServerSideEncryption": "AES256",
    "Metadata": {
        "env": "Dev",
        "author": "Alice",
        "meta": "Data"
    }
}
```

## Add Tags to an Object
Tags are another form of metadata (separate from user metadata)
```sh
aws s3api put-object-tagging \
  --bucket metadata-example-001 \
  --key file.txt \
  --tagging 'TagSet=[{Key=Project,Value=Demo},{Key=Env,Value=Dev}]'
```
## View Tags
```sh
aws s3api get-object-tagging \
  --bucket metadata-example-001 \
  --key file.txt
```
```sh
{
    "TagSet": [
        {
            "Key": "Project",
            "Value": "Demo"
        },
        {
            "Key": "Env",
            "Value": "Dev"
        }
    ]
}
```

## Upload More Files with Metadata (for Aggregation)

```sh
echo "metadataA" > fileA.txt
echo "metadataB" > fileB.txt
```
```sh

aws s3api put-object \
  --bucket metadata-example-001 \
  --key group1/fileA.txt \
  --body fileA.txt \
  --metadata group=1

aws s3api put-object \
  --bucket metadata-example-001 \
  --key group2/fileB.txt \
  --body fileB.txt \
  --metadata group=2
```

## List Objects with Prefix
```sh
aws s3api list-objects-v2 \
  --bucket metadata-example-001 \
  --prefix group1/
```

## Copy an Object and Modify Metadata
```sh
aws s3api copy-object \
  --bucket metadata-example-001 \
  --copy-source metadata-example-001/file.txt \
  --key file_copy.txt \
  --metadata Author=Bob \
  --metadata-directive REPLACE
```
Before
```sh
aws s3api head-object \
  --bucket metadata-example-001 \
  --key file.txt
```
```sh
{
    "AcceptRanges": "bytes",
    "LastModified": "2025-05-27T14:02:45+00:00",
    "ContentLength": 9,
    "ETag": "\"b3348b95d7571534c9a0b0fbc28bc5be\"",
    "ContentType": "binary/octet-stream",
    "ServerSideEncryption": "AES256",
    "Metadata": {
        "env": "Dev",
        "author": "Alice",
        "meta": "Data"
    }
}
```
After
```sh
aws s3api head-object \
  --bucket metadata-example-001 \
  --key file_copy.txt
```
```sh
{
    "AcceptRanges": "bytes",
    "LastModified": "2025-05-27T14:07:11+00:00",
    "ContentLength": 9,
    "ETag": "\"b3348b95d7571534c9a0b0fbc28bc5be\"",
    "ContentType": "binary/octet-stream",
    "ServerSideEncryption": "AES256",
    "Metadata": {
        "author": "Bob"
    }
}
```
## 🚫 Metadata Limitations

    Metadata is immutable after upload unless the object is overwritten or copied.

    Metadata values are strings only.

    AWS does not support server-side filtering by metadata (you must do it client-side).

## Clean up
```sh
aws s3 rm "s3://metadata-example-001/" --recursive --output text
aws s3api delete-bucket --bucket metadata-example-001
```