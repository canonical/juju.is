from webapp.app import app
from unittest.mock import patch
import unittest
import requests


class AssetsProxyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch("requests.get")
    def test_assets_proxy_valid_image(self, mock_get):
        response = requests.Response()
        response.headers["Content-Type"] = "image/jpeg"
        response._content = b"image content"
        mock_get.return_value = response

        response = self.app.get(
            "/assets?url=https://discourse-charmhub-io.s3.eu-west-2"
            ".amazonaws.com/image.jpg"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/jpeg")
        self.assertEqual(response.data, b"image content")

    @patch("requests.get")
    def test_assets_proxy_invalid_image(self, mock_get):
        response = requests.Response()
        response.headers["Content-Type"] = "image/jpeg"
        response._content = b"image content"
        mock_get.return_value = response

        response = self.app.get("/assets?url=http://example.com/image.jpg")
        self.assertEqual(response.status_code, 404)

    @patch("requests.get")
    def test_assets_proxy_invalid_url(self, mock_get):
        response = requests.Response()
        response.headers["Content-Type"] = "image/jpeg"
        response._content = b"image content"
        mock_get.return_value = response

        response = self.app.get("/assets?url=invalid-url")
        self.assertEqual(response.status_code, 404)

    @patch("requests.get")
    def test_assets_proxy_invalid_content_type(self, mock_get):
        response = requests.Response()
        response.headers["Content-Type"] = "text/html"
        response._content = b"image content"
        mock_get.return_value = response

        response = self.app.get(
            "/assets?url=https://discourse-charmhub-io.s3.eu-west-2"
            ".amazonaws.com/badtype.html"
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
