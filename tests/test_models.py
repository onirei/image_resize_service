from django.test import TestCase
from img_resizer.models import Image


class ModelTest(TestCase):

    def setUp(self):
        Image.objects.create(id='1', image = 'img/test1.jpg', img_hash = '123')

    def test_image_label(self):
        author=Image.objects.get(id=1)
        field_label = author._meta.get_field('image').verbose_name
        self.assertEquals(field_label,'image')

    def test_image_upload_to(self):
        author=Image.objects.get(id=1)
        field_label = author._meta.get_field('image').upload_to
        self.assertEquals(field_label,'img')

    def test_img_hash_label(self):
        author = Image.objects.get(id=1)
        field_label = author._meta.get_field('img_hash').verbose_name
        self.assertEquals(field_label, 'img hash')

    def test_img_hash_max_length(self):
        author=Image.objects.get(id=1)
        max_length = author._meta.get_field('img_hash').max_length
        self.assertEquals(max_length,32)

    def test_image_get(self):
        image=Image.objects.get(id=1)
        image = image.image
        self.assertEquals(image,'img/test1.jpg')

    def test_image_url_get(self):
        image=Image.objects.get(id=1)
        image = image.image.url
        self.assertEquals(image,'/media/img/test1.jpg')

    def test_img_hash_get(self):
        image=Image.objects.get(id=1)
        img_hash = image.img_hash
        self.assertEquals(img_hash, '123')