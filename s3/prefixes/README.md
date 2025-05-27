## Create bucket
```sh
aws s3 mb s3://prefixes-example-001
```

## Create folder
```sh
aws s3api put-object --bucket prefixes-example-001 --key hello/
```

## Create many folders
The limit is 1025 bytes, we generated 1024 bytes of lorem ipsum.
```sh
aws s3api put-object --bucket prefixes-example-001 --key Lorem/ipsum/dolor/sit/amet/consectetur/adipiscing/elit/Proin/sed/lectus/sed/nibh/sagittis/tempus/Orci/varius/natoque/penatibus/et/magnis/dis/parturient/montes/nascetur/ridiculus/mus/Suspendisse/convallis/eros/quis/sollicitudin/porttitor/Phasellus/at/turpis/feugiat/aliquet/velit/sed/consectetur/turpis/Quisque/gravida/quam/non/ante/ultrices/eu/egestas/tortor/sollicitudin/Maecenas/aliquam/mi/lectus/non/pellentesque/magna/tincidunt/quis/Duis/sit/amet/est/vel/libero/sollicitudin/elementum/Maecenas/at/dolor/ut/erat/blandit/efficitur/Sed/efficitur/vestibulum/arcu/sed/convallis/orci/ultrices/sit/amet/Proin/feugiat/eu/libero/et/ultricies/Maecenas/nunc/nibh/gravida/in/aliquet/a/gravida/et/nisl/In/in/commodo/elit/Donec/tristique/est/vel/tristique/consequat/erat/dui/eleifend/diam/a/congue/dolor/urna/vitae/ipsum/Mauris/suscipit/mauris/quis/mauris/sagittis/dapibus/Integer/eget/lacinia/augue/Etiam/sed/velit/posuere/suscipit/quam/a/facilisis/dolor/Vestibulum/in/scelerisque/orci/ac/iaculis/biam/efficutort/velit/convallis/
```
```sh
{
    "ETag": "\"d41d8cd98f00b204e9800998ecf8427e\"",
    "ChecksumCRC64NVME": "AAAAAAAAAAA=",
    "ChecksumType": "FULL_OBJECT",
    "ServerSideEncryption": "AES256"
}
```

## Try to break the 1024 limit

```sh
aws s3api put-object --bucket prefixes-example-001 --key Lorem/ipsum/dolor/sit/amet/consectetur/adipiscing/elit/Proin/sed/lectus/sed/nibh/sagittis/tempus/Orci/varius/natoque/penatibus/et/magnis/dis/parturient/montes/nascetur/ridiculus/mus/Suspendisse/convallis/eros/quis/sollicitudin/porttitor/Phasellus/at/turpis/feugiat/aliquet/velit/sed/consectetur/turpis/Quisque/gravida/quam/non/ante/ultrices/eu/egestas/tortor/sollicitudin/Maecenas/aliquam/mi/lectus/non/pellentesque/magna/tincidunt/quis/Duis/sit/amet/est/vel/libero/sollicitudin/elementum/Maecenas/at/dolor/ut/erat/blandit/efficitur/Sed/efficitur/vestibulum/arcu/sed/convallis/orci/ultrices/sit/amet/Proin/feugiat/eu/libero/et/ultricies/Maecenas/nunc/nibh/gravida/in/aliquet/a/gravida/et/nisl/In/in/commodo/elit/Donec/tristique/est/vel/tristique/consequat/erat/dui/eleifend/diam/a/congue/dolor/urna/vitae/ipsum/Mauris/suscipit/mauris/quis/mauris/sagittis/dapibus/Integer/eget/lacinia/augue/Etiam/sed/velit/posuere/suscipit/quam/a/facilisis/dolor/Vestibulum/in/scelerisque/orci/ac/iaculis/biam/efficutort/velit/convallis/myfile.txt --body myfile.txt
```
```sh
An error occurred (KeyTooLongError) when calling the PutObject operation: Your key is too long
```

## Clean up

```sh
aws s3 rm s3://prefixes-example-001/ --recursive
aws s3api delete-bucket --bucket prefixes-example-001
```