import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from books.models import Book

BOOK_URL = reverse("book:book-list")


class BookImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@admin", "password"
        )
        self.client.force_authenticate(self.user)
        self.book = Book.objects.create(
            title="TestBook",
            authors="Author Test",
            cover="Hard",
            inventory=3,
            daily_fee="10.10"
        )
        self.url = reverse("book:book-upload-image", args=[self.book.id])
        self.detail_url = reverse("book:book-detail", args=[self.book.id])

    def upload_image(self):
        """Helper function to upload an image"""
        with tempfile.NamedTemporaryFile(suffix=".jpg") as nft:
            img = Image.new("RGB", (20, 20))
            img.save(nft, format="JPEG")
            nft.seek(0)
            res = self.client.post(self.url, {"image": nft}, format="multipart")
        return res

    def test_upload_image_to_book(self):
        """Test uploading an image to book"""
        res = self.upload_image()
        self.book.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.book.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        res = self.client.post(self.url, {"image": "bad image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_is_shown_on_book_detail_page(self):
        self.upload_image()
        res = self.client.get(self.detail_url)

        self.assertIn("image", res.data)
