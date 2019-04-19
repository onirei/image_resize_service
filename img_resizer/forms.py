from django import forms


class DownloadImage(forms.Form):
    image_from_file = forms.ImageField(label='Сохранить из файла', required=False)
    image_from_url = forms.CharField(label='Сохранить по ссылке', max_length=264, required=False)
