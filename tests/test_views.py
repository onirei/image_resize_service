from django.test import TestCase
from img_resizer.models import Image
from rest_framework import status
import shutil


class ImageViewTest(TestCase):

    def setUp(self):
        shutil.copyfile('media/img/test1.jpg', 'media/img/test0.jpg')
        Image.objects.create(id='1', image = 'img/test0.jpg', img_hash = '123')

    def test_view_url_exists_show_image_list(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_show_image_list_page1(self):
        resp = self.client.get('/?page=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_download_image(self):
        resp = self.client.get('/upload/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_at_show_image(self):
        resp = self.client.get('/123/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_at_show_image_param(self):
        resp = self.client.get('/123/?width=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_at_show_image_params(self):
        resp = self.client.get('/123/?width=1&height=1&size=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_del_image(self):
        resp = self.client.get('/delete/1/')
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)






