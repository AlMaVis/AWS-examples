# AWS STS AssumeRole Hands-On Reference

This document summarizes a hands-on experience with AWS STS AssumeRole for temporary cross-account or cross-user access. The steps and commands are collected as a reference for future AWS projects and AWS Solutions Architect certification preparation. For detailed explanations, refer to the official AWS documentation linked below.

---

## User and Credentials Preparation

- **Create a user with no permissions and generate access keys:**  
  ```sh
  aws iam create-user --user-name sts-example-user
  aws iam create-access-key --user-name sts-example-user --output table
  ```
  [Creating IAM Users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)

- **Configure the credentials:**  
  ```sh
  aws configure
  ```
  Edit your AWS credentials file to use a named profile (e.g., `sts`).

- **Test identity and permissions:**  
  ```sh
  aws sts get-caller-identity --profile sts
  aws s3 ls --profile sts
  ```
  Expect an AccessDenied error for S3, since no permissions are attached.

---

## Role and Resource Setup

- **Deploy the CloudFormation stack to create a role and S3 bucket:**  
  ```sh
  chmod u+x bin/deploy
  ./bin/deploy
  ```
  [AWS CloudFormation Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)

- **Role and bucket are defined in [`iam-role.yaml`](iam-role.yaml).**  
  The role allows the user to assume it and grants S3 access to the specified bucket.

---

## Policy Attachment

- **Attach an inline policy to allow the user to assume the role:**  
  ```sh
  aws iam put-user-policy \
    --user-name sts-example-user \
    --policy-name StsPolicy \
    --policy-document file://policy.json
  ```
  [IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)

---

## Assume Role and Use Temporary Credentials

- **Get the role name from CloudFormation:**  
  ```sh
  aws cloudformation describe-stack-resources --stack-name sts-example
  ```

- **Assume the role using STS:**  
  ```sh
  aws sts assume-role \
    --role-arn arn:aws:iam::<account-id>:role/<role-name> \
    --role-session-name s3-sts-example \
    --profile sts
  ```
  [AWS STS AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)

- **Set the returned credentials as a new profile (`assumed`) in your AWS credentials file.**

- **Verify the assumed identity:**  
  ```sh
  aws sts get-caller-identity --profile assumed
  ```

- **Access the S3 bucket with the assumed role:**  
  ```sh
  aws s3 ls s3://sts-example-bucket-001 --profile assumed
  ```

---

## Key Points

- Demonstrates the use of IAM users, roles, and policies for secure, temporary access.
- Shows how to use AWS STS to assume a role and access resources with temporary credentials.
- CloudFormation is used for reproducible resource and role setup.

---

## Cleanup

To remove all resources created during this hands-on:

- **Delete the CloudFormation stack (removes the role and S3 bucket):**
  ```sh
  aws cloudformation delete-stack --stack-name sts-example
  ```

- **Delete the IAM user:**
  ```sh
  aws iam delete-user-policy --user-name sts-example-user --policy-name StsPolicy
  aws iam delete-access-key --user-name sts-example-user --access-key-id AKIARMEKEFD7XUFCOEZC
  aws iam delete-user --user-name sts-example-user
  ```

- **Remove any local AWS CLI credentials/profiles you created for this test.**

---

## References

- [AWS STS AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
- [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
- [AWS CLI S3 Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html)