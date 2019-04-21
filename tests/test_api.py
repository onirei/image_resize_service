import shutil
from rest_framework import status
from rest_framework.test import APITestCase
from img_resizer.models import Image


class ApiV1Test(APITestCase):

    base_url = 'http://localhost:8000/api_v1/'

    def setUp(self):
        shutil.copyfile('media/img/test1.jpg', 'media/img/test0.jpg')
        self.record = Image.objects.create(id='1', image = 'img/test0.jpg',
                                           img_hash = '123')

    def test_get(self):
        url = self.base_url + 'images/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_file(self):
        url = self.base_url + 'images/'
        files = {'file': open(r'media/img/test1.jpg', 'br')}
        response = self.client.post(url, files)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_url_http(self):
        url = self.base_url + 'images/'
        data = {'url': 'http://www.colordigits.ru/testimages/Inktest_V2-1.jpg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_url_https(self):
        url = self.base_url + 'images/'
        data = {'url': 'https://pp.userapi.com/c851224/v851224831/fe082/MKRaJbCH_6c.jpg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_400(self):
        url = self.base_url + 'images/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_resize_by_hash(self):
        url = self.base_url + 'images/123/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_resize_by_hash_with_1_params(self):
        url = self.base_url + 'images/123/'
        params = {'width': 300}
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_resize_by_hash_with_all_params(self):
        url = self.base_url + 'images/123/'
        params = {'width': 300, 'height':300, 'size':300}
        response = self.client.get(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_resize_by_hash_404(self):
        url = self.base_url + 'images/1234/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_del_by_hash(self):
        url = self.base_url + 'images/123/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_del_by_hash_(self):
        url = self.base_url + 'images/1234/'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)