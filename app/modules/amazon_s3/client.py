from logging import Logger
import mimetypes
import boto3

from app.config import Config


logger = Logger(__name__)


class AmazonS3Client:
    def __init__(self) -> None:
        try:
            self.client = boto3.client(
                "s3",
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                region_name=Config.AWS_REGION,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Amazon S3 client: {e}")
            raise e

    def upload_image(self, local_path: str, bucket_name: str, s3_key: str) -> str:
        content_type: str | None
        content_type, _ = mimetypes.guess_type(local_path)
        try:
            self.client.upload_file(
                local_path,
                bucket_name,
                s3_key,
                ExtraArgs={"ContentType": content_type or "application/octet-stream"},
            )
        except Exception as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise e

        return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
