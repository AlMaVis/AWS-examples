## Create a bucket
```sh
aws s3 mb s3://class-change-example-001
```

## Create a file
```sh
echo "class change" >> myfile.txt
```

## Upload the file
```sh
aws s3 cp myfile.txt s3://class-change-example-001
```