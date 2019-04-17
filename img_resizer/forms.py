from django import forms


class DownloadImage(forms.Form):
    image_from_file = forms.ImageField(required=False)
    image_from_url = forms.CharField(label='Название заявки', max_length=264, required=False)
