import uuid
import os
from datetime import timedelta
from google.cloud import storage
from google.api_core.exceptions import NotFound, PermissionDenied

BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

def upload_media_to_gcs(file_bytes: bytes, file_extension: str) -> str:
    if not BUCKET_NAME:
        raise RuntimeError("GCS_BUCKET_NAME is not set in environment variables.")

    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)

        # Determine media type
        if file_extension.lower() in ["png", "jpg", "jpeg", "webp"]:
            folder = "generated/generatedImage"
            content_type = f"image/{file_extension}"
        else:
            folder = "generated/generatedVideo"
            content_type = f"video/{file_extension}"

        file_name = f"{folder}/{uuid.uuid4()}.{file_extension}"
        blob = bucket.blob(file_name)

        blob.upload_from_string(file_bytes, content_type=content_type)

        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=7),
            method="GET"
        )

        print(f"[GCS Service] Uploaded to: {signed_url}")
        return signed_url

    except NotFound:
        raise RuntimeError(
            f"GCS bucket '{BUCKET_NAME}' not found. Create it in Google Cloud Console."
        )
    except PermissionDenied:
        raise RuntimeError(
            f"Permission denied for bucket '{BUCKET_NAME}'. "
            f"Check service account permissions."
        )
    except Exception as e:
        raise RuntimeError(f"GCS Upload Failed: {e}")
