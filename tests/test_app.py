from unittest.mock import patch, MagicMock, mock_open
from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)


@patch("app.app.deepseek_client.request", return_value="Generated article")
def test_create_article_all_paths(mock_request):
    payload = {
        "topic": "AI and Ethics",
        "length": 500,
        "requirements": "Be clear and concise.",
        "reference": "https://example.com",
        "output_format": "html"
    }

    response = client.post("/create-article", json=payload)
    assert response.status_code == 200

    result = response.json()
    assert "result" in result
    assert result["result"] == "Generated article".replace("\n", "")
    mock_request.assert_called_once()

    payload["output_format"] = "markdown"
    response = client.post("/create-article", json=payload)
    assert response.status_code == 200
    mock_request.assert_called()


@patch("app.app.amazon_s3_client.upload_image", return_value="https://s3.amazonaws.com/fake/image.jpg")
@patch("app.app.requests.get")
@patch("app.app.openai_client.request", return_value="https://image.url/fake.jpg")
@patch("app.app.os.makedirs")
@patch("app.app.os.remove")
@patch("app.app.shutil.rmtree")
@patch("app.app.open", new_callable=mock_open)
@patch("app.app.os.path.exists", side_effect=[True, True])
def test_create_image_all_paths(
    mock_exists,
    mock_file,
    mock_rmtree,
    mock_remove,
    mock_makedirs,
    mock_openai_request,
    mock_requests_get,
    mock_upload_image
):
    mock_response = MagicMock()
    mock_response.content = b"fake_image_data"
    mock_requests_get.return_value = mock_response

    payload = {
        "description": "Generate a photo",
        "width": 512,
        "height": 512,
        "quality": "high",
        "amazon_s3_bucket": "my-bucket",
        "amazon_s3_path": "media/"
    }

    response = client.post("/create-image", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["url"].startswith("https://s3.amazonaws.com")

    mock_openai_request.assert_called_once()
    mock_requests_get.assert_called_once_with("https://image.url/fake.jpg")
    mock_upload_image.assert_called_once()
    mock_makedirs.assert_called_once()
    mock_file.assert_called_once()
    mock_remove.assert_called_once()
    mock_rmtree.assert_called_once()
    assert mock_exists.call_count == 2
