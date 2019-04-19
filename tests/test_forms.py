from django.test import TestCase
from img_resizer.forms import DownloadImage


class FormTest(TestCase):

    def test_form_file_field_label(self):
        form = DownloadImage()
        self.assertTrue(not form.fields['image_from_file'].label or form.fields['image_from_file'].label == 'Сохранить из файла')

    def test_form_url_field_label(self):
        form = DownloadImage()
        self.assertTrue(not form.fields['image_from_url'].label or form.fields['image_from_url'].label == 'Сохранить по ссылке')

    def test_form_url_field_max_length(self):
        form = DownloadImage()
        self.assertEquals(form.fields['image_from_url'].max_length, 264)

    def test_form_file_valid(self):
        img = 'media/img/test1.jpg'
        form_data = {'image_from_file': img}
        form = DownloadImage(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_url_valid(self):
        img = 'http://site.com/test.jpg'
        form_data = {'image_from_url': img}
        form = DownloadImage(data=form_data)
        self.assertTrue(form.is_valid())