import os
import requests
import hashlib
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.conf import settings
from django.views.decorators.cache import cache_page
from PIL import Image as Image_PIL
from img_resizer.models import Image
from img_resizer.forms import DownloadImage


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


@cache_page(600, cache='default', key_prefix='')
def show_image(request, img_hash):
    img_obj = Image.objects.get(img_hash=img_hash)
    width = request.GET.get('width')
    height = request.GET.get('height')
    size = request.GET.get('size')
    if not width and not height and not size:
        params = {'width': img_obj.image.width, 'height': img_obj.image.height,
                  'size': img_obj.image.size}
        return render(request, 'image.html', {'image': img_obj,
                                              'params': params})
    else:
        if not width:
            width = img_obj.image.width
        if not height:
            height = img_obj.image.height
        if not size:
            size = img_obj.image.size

        path = img_obj.image.name.replace('/','.').split('.')
        path = '{}{}{}_w{}_h{}_s{}.{}'.format(
            settings.MEDIA_URL[1:], settings.MEDIA_HASH_URL,
            path[-2], str(width), str(height), str(size), path[-1]
            )

        if os.path.isfile(path):
            img = Image_PIL.open(path)
            img_size = len(img.fp.read())
        else:
            img = Image_PIL.open(img_obj.image.url[1:])
            img = img.resize((int(width),int(height)), Image_PIL.ANTIALIAS)
            img.save(path, quality=75)

            img = Image_PIL.open(path)
            img_size = len(img.fp.read())
            img.save(path)
            q = 75
            while img_size > int(size) and q >= 1:
                img = Image_PIL.open(path)
                img_size = len(img.fp.read())
                img.save(path, quality=q)
                q += -1

        params = {'width': width, 'height': height, 'size': img_size}
        path = ''.join(['/', path])
        return render(request, 'image.html', {'img': path,
                                              'params': params})


def del_image(request, pk):
    task_obj = Image.objects.get(id=pk)
    os.remove(task_obj.image.path)
    task_obj.delete()
    return HttpResponseRedirect('/')


def download_handler(url):
    r = requests.get(url, stream=True)
    path = settings.MEDIA_URL[1:]
    file_name = '{}/{}'.format(Image._meta.get_field('image').upload_to,
                               url.split('/')[-1])
    file_path = path + file_name
    with open(file_path, 'bw') as file:
        for chunk in r.iter_content(2048):
            file.write(chunk)
    return file_name


def download_image(request):
    if request.POST:
        form = DownloadImage(request.POST, request.FILES)
        if (form.is_valid() and form.cleaned_data['image_from_file'] and
                    '_file' in request.POST):
            image_obj = Image()
            image_obj.image = form.cleaned_data['image_from_file']
            img = Image_PIL.open(image_obj.image)
            image_obj.img_hash = hashlib.md5(img.tobytes()).hexdigest()
            # Переписать блок на проверку вхождения мд5
            try:
                image_obj.save()
                return HttpResponseRedirect('/')
            except IntegrityError:
                form = DownloadImage()
                error = 'Этот файл уже загружен на сервер'
                return render(request, 'upload.html',
                              {'form': form, 'error': error})
        elif (form.is_valid() and form.cleaned_data['image_from_url'] and
                      '_url' in request.POST):
            image_obj = Image()
            image_obj.image = download_handler(
                form.cleaned_data['image_from_url']
            )
            img = Image_PIL.open(image_obj.image)
            image_obj.img_hash = hashlib.md5(img.tobytes()).hexdigest()
            # Переписать блок на проверку вхождения мд5
            try:
                image_obj.save()
                return HttpResponseRedirect('/')
            except IntegrityError:
                form = DownloadImage()
                error = 'Этот файл уже загружен на сервер'
                return render(request, 'upload.html', {'form': form,
                                                       'error': error})
    else:
        form = DownloadImage()
    return render(request, 'upload.html', {'form': form})
