# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
This example sets up the Raw AES Keyring

The Raw AES keyring uses customer-provided symmetric encryption keys to generate, encrypt and
decrypt data keys. This example creates a Raw AES Keyring and then encrypts a custom input EXAMPLE_DATA
with an encryption context. This example also includes some sanity checks for demonstration:
1. Ciphertext and plaintext data are not the same
2. Encryption context is correct in the decrypted message header
3. Decrypted plaintext value matches EXAMPLE_DATA
These sanity checks are for demonstration in the example only. You do not need these in your code.

Raw AES keyrings can be used independently or in a multi-keyring with other keyrings
of the same or a different type.

"""

import boto3
from aws_cryptographic_material_providers.mpl import AwsCryptographicMaterialProviders
from aws_cryptographic_material_providers.mpl.config import MaterialProvidersConfig
from aws_cryptographic_material_providers.mpl.models import CreateRawAesKeyringInput, AesWrappingAlg

from typing import Dict
import base64
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
import argparse

EXAMPLE_DATA: bytes = b"Hello World"
BUCKET_NAME = "encryption-client-side-example-001"
OBJECT_KEY = "myfile.txt"
REGION = "eu-west-3"
KEY_NAME_SPACE = "HSM_01"
KEY_NAME = "AES_256_012"


def get_raw_key(key_b64: str) -> bytes:
    return base64.b64decode(key_b64)


def encrypt_and_upload(raw_key_b64: str):
    client = aws_encryption_sdk.EncryptionSDKClient(
        commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
    )
    s3_client = boto3.client('s3', region_name=REGION)

    encryption_context: Dict[str, str] = {
        "example": "client-side raw key"
    }

    mat_prov = AwsCryptographicMaterialProviders(config=MaterialProvidersConfig())
    raw_key = get_raw_key(raw_key_b64)
    keyring_input = CreateRawAesKeyringInput(
        key_namespace=KEY_NAME_SPACE,
        key_name=KEY_NAME,
        wrapping_key=raw_key,
        wrapping_alg=AesWrappingAlg.ALG_AES256_GCM_IV12_TAG16
    )
    raw_keyring = mat_prov.create_raw_aes_keyring(input=keyring_input)

    ciphertext, _ = client.encrypt(
        source=EXAMPLE_DATA,
        keyring=raw_keyring,
        encryption_context=encryption_context
    )

    # Upload ciphertext to S3
    s3_client.put_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY, Body=ciphertext)
    print(f"Encrypted data uploaded to s3://{BUCKET_NAME}/{OBJECT_KEY}")


def download_and_decrypt(raw_key_b64: str):
    client = aws_encryption_sdk.EncryptionSDKClient(
        commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
    )
    s3_client = boto3.client('s3', region_name=REGION)

    mat_prov = AwsCryptographicMaterialProviders(config=MaterialProvidersConfig())
    raw_key = get_raw_key(raw_key_b64)
    keyring_input = CreateRawAesKeyringInput(
        key_namespace=KEY_NAME_SPACE,
        key_name=KEY_NAME,
        wrapping_key=raw_key,
        wrapping_alg=AesWrappingAlg.ALG_AES256_GCM_IV12_TAG16
    )
    raw_keyring = mat_prov.create_raw_aes_keyring(input=keyring_input)

    # Download ciphertext from S3
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
    ciphertext = response['Body'].read()

    # Decrypt
    plaintext_bytes, _ = client.decrypt(
        source=ciphertext,
        keyring=raw_keyring
    )
    print("Decrypted plaintext:", plaintext_bytes.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt/Decrypt with Raw AES Keyring and S3")
    parser.add_argument("mode", choices=["upload", "download"], help="upload or download")
    parser.add_argument("--raw-key-b64", required=True, help="Base64-encoded 256-bit AES key")
    args = parser.parse_args()

    if args.mode == "upload":
        encrypt_and_upload(args.raw_key_b64)
    elif args.mode == "download":
        download_and_decrypt(args.raw_key_b64)

