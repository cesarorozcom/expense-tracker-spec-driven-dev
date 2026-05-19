"""
S3-compatible object storage backend for invoice photos.

Uses django-storages and boto3 to provide secure, signed-URL-based access
to invoice photos stored in S3-compatible object storage (AWS S3, MinIO, etc).
"""

import os
from storages.backends.s3boto3 import S3Boto3Storage


class InvoicePhotoStorage(S3Boto3Storage):
    """
    S3-compatible storage backend for invoice photo uploads.
    
    Configuration:
    - AWS_ACCESS_KEY_ID: S3 access key (from environment)
    - AWS_SECRET_ACCESS_KEY: S3 secret key (from environment)
    - AWS_STORAGE_BUCKET_NAME: Bucket name for invoice photos
    - AWS_S3_REGION_NAME: AWS region (default: us-east-1)
    - AWS_S3_ENDPOINT_URL: S3-compatible endpoint (optional, for MinIO/other providers)
    - AWS_S3_CUSTOM_DOMAIN: Custom domain for CDN (optional)
    - AWS_S3_OBJECT_PARAMETERS: Additional S3 parameters (e.g., CannedACL, ServerSideEncryption)
    
    Usage:
    - Set MEDIA_ROOT and DEFAULT_FILE_STORAGE in settings.py to use this backend
    - Supports direct-to-S3 signed upload flows (via boto3 client)
    - Files are encrypted-at-rest by default (SSE-S3)
    - Access via short-lived signed URLs (default: 3600 seconds)
    """

    # Default location for uploaded photos within the bucket
    location = "receipts"

    # File permissions: private (not publicly readable)
    file_overwrite = False
    default_acl = "private"

    # Signed URL expiration time (1 hour)
    url_expiration = 3600

    @property
    def location(self):
        """Allow override of bucket location via PHOTO_STORAGE_LOCATION env var."""
        return os.environ.get("PHOTO_STORAGE_LOCATION", "receipts")

    def _get_key(self, name):
        """Override to support custom S3 object parameters (encryption, etc)."""
        key = super()._get_key(name)
        # Ensure encryption-at-rest is enabled (SSE-S3)
        if not key.server_side_encryption:
            key.server_side_encryption = "AES256"
        return key


class PublicMediaStorage(S3Boto3Storage):
    """
    Alternative storage backend for public/non-sensitive files (future use).
    Not used in v1 invoice photo implementation but available for future expansion.
    """
    location = "public"
    default_acl = "public-read"
