from django import forms
from img_resizer.models import Image


class DownloadImage(forms.ModelForm):
    image_from_file = forms.ImageField(label='Сохранить из файла',
                                       required=False)
    image_from_url = forms.CharField(label='Сохранить по ссылке',
                                     max_length=264, required=False)

    class Meta:
        model = Image
        fields = [
            'image_from_file',
            'image_from_url'
        ]
        labels = {
            'image_file': 'File',
            'image_url': 'URL'
        }
