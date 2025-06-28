# Terraform AWS VPC and Network ACL Example

This Terraform project creates a basic AWS VPC with a Network ACL (NACL) using good practices.

---

## Features

- Creates a VPC with DNS support and hostnames enabled
- Creates a Network ACL attached to the VPC
- Adds simple rules to allow inbound and outbound HTTP (port 80) traffic
- Uses variables for flexibility
- Provides outputs for important resource IDs

---

## Prerequisites

- Terraform >= 1.12.1
- AWS CLI configured with credentials
- AWS account with permissions to create VPCs and NACLs

---

## Usage

1. Clone the repository:

    ```sh
    git clone <repository_url>
    cd terraform-vpc-nacl
    ```

2. Initialize Terraform:

    ```sh
    terraform init
    ```

3. Review the planned changes:

    ```sh
    terraform plan
    ```

4. Apply the configuration:

    ```sh
    terraform apply
    ```

5. Confirm and wait for resources to be created.

6. Use the output values to reference your VPC and NACL IDs.

---

## Variables

| Name         | Description                  | Default     |
|--------------|------------------------------|-------------|
| `aws_region` | AWS region to deploy resources| `us-east-1` |
| `vpc_cidr`   | CIDR block for the VPC        | `10.0.0.0/16` |
| `nacl_name`  | Name tag for the Network ACL  | `example-nacl` |

---
## AWS CLI Commands

Inspect and verify the created resources.

1. List all VPCs:

    ```sh
    aws ec2 describe-vpcs --query "Vpcs[*].{ID:VpcId,CIDR:CidrBlock,IsDefault:IsDefault}" --output table
    ```

2. List all NACLs:

    ```sh
    aws ec2 describe-network-acls --query "NetworkAcls[*].{ID:NetworkAclId,VPC:VpcId,IsDefault:IsDefault}" --output table
    ```

3. Describe the specific NACL (use the returned id from previous output):

    ```sh
    aws ec2 describe-network-acls --network-acl-ids acl-062215a2501b5979b
    ```

4. View NACL entries\rules
    ```sh
    aws ec2 describe-network-acls \
    --network-acl-ids acl-062215a2501b5979b \
    --query "NetworkAcls[*].Entries[*].{RuleNumber:RuleNumber,Egress:Egress,Protocol:Protocol,RuleAction:RuleAction,CIDR: CidrBlock,Ports:[PortRange.From, PortRange.To]}" \
    --output table
    ```

## Notes

- This example uses minimal NACL rules for demonstration. Adjust inbound/outbound rules based on your security requirements.
- AWS Network ACLs are stateless; ensure rules are mirrored for inbound and outbound traffic where necessary.
- For production, consider additional layers like security groups and flow logs.

---

## Cleanup

To destroy all resources:

```sh
terraform destroy
```
