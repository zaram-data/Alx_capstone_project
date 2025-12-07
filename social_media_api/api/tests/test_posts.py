ffrom rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Post

class PostTests(APITestCase):

    def test_create_post(self):
        url = reverse('post-list')
        data = {"content": "Hello world!"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_get_posts(self):
        Post.objects.create(content="Sample post")
        url = reverse('post-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
