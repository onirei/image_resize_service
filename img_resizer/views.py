from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from .models import Image
from .forms import DownloadImage
import requests


def show_image_list(request):
    image_list = Image.objects.all().order_by('id')
    paginator = Paginator(image_list, 10)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return render_to_response('index.html', {'images': images})


def show_image(request, img_id):
    image_obj = Image.objects.get(id=img_id)
    return render(request, 'image.html', {'image':image_obj})


def download_handler(url):
    r = requests.get(url, stream=True)
    path = 'media/'
    filename = 'img/'+url.split('/')[-1]
    with open(path+filename, 'bw') as file:
        for chunk in r.iter_content(2048):
            file.write(chunk)
    return filename

def download_image(request):
    if request.POST:
        form = DownloadImage(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['image_from_file']:
            image_obj = Image()
            image_obj.image = form.cleaned_data['image_from_file']
            image_obj.save()
            return HttpResponseRedirect('/')
        elif form.is_valid() and form.cleaned_data['image_from_url']:
            image_obj = Image()
            image_obj.image = download_handler(form.cleaned_data['image_from_url'])
            image_obj.save()
            return HttpResponseRedirect('/')
    else:
        form = DownloadImage()
    return render(request, 'upload.html', {'form': form})