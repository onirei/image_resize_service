from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from .models import Image
from .forms import DownloadImage
import requests
import hashlib
from PIL import Image as Image_PIL


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


def show_image(request, img_hash):
    img = Image.objects.get(img_hash=img_hash)
    width = request.GET.get('width')
    height = request.GET.get('height')
    size = request.GET.get('size')
    if not width and not height and not size:
        return render(request, 'image.html', {'image': img})
    else:
        params = [width, height, size]

        return render(request, 'image.html', {'params': params})


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
            img = Image_PIL.open(image_obj.image)
            image_obj.img_hash = hashlib.md5(img.tobytes()).hexdigest()
            image_obj.save()
            return HttpResponseRedirect('/')
        elif form.is_valid() and form.cleaned_data['image_from_url']:
            image_obj = Image()
            image_obj.image = download_handler(form.cleaned_data['image_from_url'])
            img = Image_PIL.open(image_obj.image)
            image_obj.img_hash = hashlib.md5(img.tobytes()).hexdigest()
            image_obj.save()
            return HttpResponseRedirect('/')
    else:
        form = DownloadImage()
    return render(request, 'upload.html', {'form': form})
