# AWS S3 CORS Hands-On Reference

This document summarizes a hands-on experience configuring two AWS S3 buckets for static website hosting and enabling cross-origin resource sharing (CORS) between them. It serves as a reference for future AWS projects and AWS Solutions Architect certification.

---

## Website 1: Static Hosting and Public Access

- **Bucket creation:**  
  ```sh
  aws s3 mb s3://cors-example-0001
  ```
  [AWS CLI: aws s3 mb](https://docs.aws.amazon.com/cli/latest/reference/s3/mb.html)

- **Block public access settings:**  
  ```sh
  aws s3api put-public-access-block \
    --bucket cors-example-0001 \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false"
  ```
  [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

- **Bucket policy for public read:**  
  See `bucket-policy.json` for the policy document.
  ```sh
  aws s3api put-bucket-policy --bucket cors-example-0001 --policy file://bucket-policy.json
  ```
  [S3 Bucket Policy Examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)

- **Enable static website hosting:**  
  See `website-conf.json` for the configuration.
  ```sh
  aws s3api put-bucket-website --bucket cors-example-0001 --website-configuration file://website-conf.json
  ```
  [Hosting a Static Website on Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)

- **Upload website content:**  
  ```sh
  aws s3 cp index1.html s3://cors-example-0001
  aws s3 cp error.html s3://cors-example-0001
  ```

- **Website endpoint format:**  
  ```
  http://cors-example-0001.s3-website.eu-west-3.amazonaws.com/
  ```

---

## Website 2: Second Static Site for CORS Testing

- **Bucket creation:**  
  ```sh
  aws s3 mb s3://cors-example-0002
  ```

- **Block public access settings:**  
  ```sh
  aws s3api put-public-access-block \
    --bucket cors-example-0002 \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false"
  ```

- **Bucket policy for public read:**  
  See `bucket-policy2.json` for the policy document.
  ```sh
  aws s3api put-bucket-policy --bucket cors-example-0002 --policy file://bucket-policy2.json
  ```

- **Enable static website hosting:**  
  See `website-conf2.json` for the configuration.
  ```sh
  aws s3api put-bucket-website --bucket cors-example-0002 --website-configuration file://website-conf2.json
  ```

- **Upload test page:**  
  ```sh
  aws s3 cp index2.html s3://cors-example-0002
  aws s3 cp error.html s3://cors-example-0002
  ```

- **Website endpoint format:**  
  ```
  http://cors-example-0002.s3-website.eu-west-3.amazonaws.com/
  ```

---

## CORS Configuration

- **CORS policy for Website 1:**  
  See `cors.json` for the configuration.  
  Example:
  ```json
  {
      "CORSRules": [
          {
              "AllowedHeaders": ["*"],
              "AllowedMethods": ["GET", "POST", "PUT"],
              "AllowedOrigins": [
                  "http://cors-example-0002.s3-website.eu-west-3.amazonaws.com"
              ],
              "ExposeHeaders": [],
              "MaxAgeSeconds": 3000
          }
      ]
  }
  ```
  [S3 CORS Configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html)

  Apply with:
  ```sh
  aws s3api put-bucket-cors --bucket cors-example-0001 --cors-configuration file://cors.json
  ```

---

## Cross-Origin Test

- **index2.html** (in Website 2) fetches `index1.html` from Website 1 using JavaScript `fetch()`.
- If CORS is configured correctly, the content of `index1.html` is displayed in Website 2.
- If not, browser blocks the request due to CORS policy.

---

## Clean up
```sh
aws s3 rb s3://cors-example-0001 --force
aws s3 rb s3://cors-example-0002 --force
```

## Summary

- S3 static website hosting requires public read access and website configuration.
- CORS must be explicitly enabled on the source bucket for cross-origin requests.
- Testing CORS between two S3-hosted sites is a practical way to understand browser security and AWS configuration.

---

## References

- [Amazon S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Amazon S3 CORS Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html)
- [Amazon S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
- [AWS CLI S3 Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html)
