from unittest.mock import patch, MagicMock
from app.modules.amazon_s3.client import AmazonS3Client

@patch("app.modules.amazon_s3.client.Config.AWS_ACCESS_KEY_ID", "fake-key-id")
@patch("app.modules.amazon_s3.client.Config.AWS_SECRET_ACCESS_KEY", "fake-secret")
@patch("app.modules.amazon_s3.client.Config.AWS_REGION", "us-fake-1")
@patch("app.modules.amazon_s3.client.boto3.client")
def test_amazon_s3_client_init(mock_boto_client):
    instance = AmazonS3Client()
    mock_boto_client.assert_called_once_with(
        "s3",
        aws_access_key_id="fake-key-id",
        aws_secret_access_key="fake-secret",
        region_name="us-fake-1",
    )
    assert hasattr(instance, "client")


@patch("app.modules.amazon_s3.client.mimetypes.guess_type", return_value=("image/jpeg", None))
@patch("app.modules.amazon_s3.client.boto3.client")
def test_upload_image(mock_boto_client, mock_guess_type):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    s3 = AmazonS3Client()
    result = s3.upload_image(
        local_path="image.jpg",
        bucket_name="my-bucket",
        s3_key="images/image.jpg"
    )

    mock_guess_type.assert_called_once_with("image.jpg")
    mock_s3.upload_file.assert_called_once_with(
        "image.jpg",
        "my-bucket",
        "images/image.jpg",
        ExtraArgs={"ContentType": "image/jpeg"},
    )

    assert result == "https://my-bucket.s3.amazonaws.com/images/image.jpg"


@patch("app.modules.amazon_s3.client.mimetypes.guess_type", return_value=(None, None))
@patch("app.modules.amazon_s3.client.boto3.client")
def test_upload_image_fallback_content_type(mock_boto_client, mock_guess_type):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    s3 = AmazonS3Client()
    result = s3.upload_image(
        local_path="unknown.ext",
        bucket_name="other-bucket",
        s3_key="files/unknown.ext"
    )

    mock_s3.upload_file.assert_called_once_with(
        "unknown.ext",
        "other-bucket",
        "files/unknown.ext",
        ExtraArgs={"ContentType": "application/octet-stream"},
    )

    assert result == "https://other-bucket.s3.amazonaws.com/files/unknown.ext"