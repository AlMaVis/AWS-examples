# Prefixes

This document demonstrates how to work with S3 object keys that simulate folders using prefixes. It explores S3’s key length limits and how prefixes enable a hierarchical organization in the flat S3 namespace.

---

## Create a new S3 bucket

```sh
aws s3 mb s3://prefixes-example-001
```

> Creates an S3 bucket named `prefixes-example-001` using the high-level `aws s3` command.
> [AWS CLI Docs: s3 mb](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/mb.html)

---

## Create a folder (prefix) in the bucket

```sh
aws s3api put-object --bucket prefixes-example-001 --key hello/
```

> Creates an empty object with key ending in `/`, which acts like a folder placeholder in S3.
> S3 is flat, but the `/` separator in keys enables tools and consoles to display a folder-like hierarchy.
> [AWS CLI Docs: s3api put-object](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/put-object.html)

---

## Create many folders with a long key (up to 1024 bytes)

```sh
aws s3api put-object --bucket prefixes-example-001 --key Lorem/ipsum/dolor/sit/amet/consectetur/adipiscing/elit/Proin/sed/lectus/sed/nibh/sagittis/tempus/Orci/varius/natoque/penatibus/et/magnis/dis/parturient/montes/nascetur/ridiculus/mus/Suspendisse/convallis/eros/quis/sollicitudin/porttitor/Phasellus/at/turpis/feugiat/aliquet/velit/sed/consectetur/turpis/Quisque/gravida/quam/non/ante/ultrices/eu/egestas/tortor/sollicitudin/Maecenas/aliquam/mi/lectus/non/pellentesque/magna/tincidunt/quis/Duis/sit/amet/est/vel/libero/sollicitudin/elementum/Maecenas/at/dolor/ut/erat/blandit/efficitur/Sed/efficitur/vestibulum/arcu/sed/convallis/orci/ultrices/sit/amet/Proin/feugiat/eu/libero/et/ultricies/Maecenas/nunc/nibh/gravida/in/aliquet/a/gravida/et/nisl/In/in/commodo/elit/Donec/tristique/est/vel/tristique/consequat/erat/dui/eleifend/diam/a/congue/dolor/urna/vitae/ipsum/Mauris/suscipit/mauris/quis/mauris/sagittis/dapibus/Integer/eget/lacinia/augue/Etiam/sed/velit/posuere/suscipit/quam/a/facilisis/dolor/Vestibulum/in/scelerisque/orci/ac/iaculis/biam/efficutort/velit/convallis/
```

```json
{
    "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
    "ChecksumCRC64NVME": "AAAAAAAAAAA=",
    "ChecksumType": "FULL_OBJECT",
    "ServerSideEncryption": "AES256"
}
```

> S3 object keys can be very long, up to 1024 bytes in length (UTF-8). This example uses a very long key with many folder-like prefixes.
> The empty object simulates nested folders, useful for some tools or user expectations.

---

## Try to exceed the 1024 byte key limit (expect failure)

```sh
aws s3api put-object --bucket prefixes-example-001 --key Lorem/ipsum/dolor/sit/amet/consectetur/adipiscing/elit/Proin/sed/lectus/sed/nibh/sagittis/tempus/Orci/varius/natoque/penatibus/et/magnis/dis/parturient/montes/nascetur/ridiculus/mus/Suspendisse/convallis/eros/quis/sollicitudin/porttitor/Phasellus/at/turpis/feugiat/aliquet/velit/sed/consectetur/turpis/Quisque/gravida/quam/non/ante/ultrices/eu/egestas/tortor/sollicitudin/Maecenas/aliquam/mi/lectus/non/pellentesque/magna/tincidunt/quis/Duis/sit/amet/est/vel/libero/sollicitudin/elementum/Maecenas/at/dolor/ut/erat/blandit/efficitur/Sed/efficitur/vestibulum/arcu/sed/convallis/orci/ultrices/sit/amet/Proin/feugiat/eu/libero/et/ultricies/Maecenas/nunc/nibh/gravida/in/aliquet/a/gravida/et/nisl/In/in/commodo/elit/Donec/tristique/est/vel/tristique/consequat/erat/dui/eleifend/diam/a/congue/dolor/urna/vitae/ipsum/Mauris/suscipit/mauris/quis/mauris/sagittis/dapibus/Integer/eget/lacinia/augue/Etiam/sed/velit/posuere/suscipit/quam/a/facilisis/dolor/Vestibulum/in/scelerisque/orci/ac/iaculis/biam/efficutort/velit/convallis/myfile.txt --body myfile.txt
```

```txt
An error occurred (KeyTooLongError) when calling the PutObject operation: Your key is too long
```

> Attempting to create an object key longer than 1024 bytes results in a `KeyTooLongError`.
> This limit applies to the entire UTF-8 encoded key string, including all prefixes and filename.
> [AWS S3 Limits Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html#object-key-guidelines)

---

## Clean up: Remove all objects and delete the bucket

```sh
aws s3 rm s3://prefixes-example-001/ --recursive
aws s3api delete-bucket --bucket prefixes-example-001
```

> Recursively deletes all objects and then removes the bucket to avoid lingering resources.
> [AWS CLI Docs: s3 rm](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/rm.html)
> [AWS CLI Docs: s3api delete-bucket](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/delete-bucket.html)

---

### Summary

This exercise demonstrates how S3 treats prefixes as part of object keys to simulate folders, the maximum allowed key length of 1024 bytes, and the resulting error when exceeding this limit. 