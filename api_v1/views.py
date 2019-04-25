import os
import hashlib
import requests
from PIL import Image as Image_PIL
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_v1.serializers import ImageSerializer
from img_resizer.models import Image


class ImageList(APIView):
    path = settings.MEDIA_URL[1:]

    def download_handler_url(self, url):
        r = requests.get(url, stream=True)
        file_name = (f"{Image._meta.get_field('image').upload_to}/"
                     f"{url.split('/')[-1]}")
        file_path = self.path + file_name
        with open(file_path, 'bw') as file:
            for chunk in r.iter_content(2048):
                file.write(chunk)
        return file_name

    def download_handler_file(self, f):
        file_name = (f"{Image._meta.get_field('image').upload_to}/"
                     f"{f.name.split('/')[-1]}")
        file_path = self.path + file_name
        with open(file_path, 'bw') as file:
            for chunk in f.chunks(2048):
                file.write(chunk)
        return file_name

    def get(self, request, format=None):
        images = Image.objects.all()
        for image in images:
            image.image = get_current_site(self.request).domain + \
                          image.image.url
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, format=None, **kwargs):
        if request.FILES:
            f = request.FILES.get('file')
            file_name = self.download_handler_file(f)
        elif request.data:
            url = request.data['url']
            file_name = self.download_handler_url(url)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        img = Image_PIL.open(self.path + file_name)
        img_hash = hashlib.md5(img.tobytes()).hexdigest()

        if Image.objects.filter(img_hash=img_hash).exists():
            error = {'error': 'Этот файл уже загружен на сервер'}
            return Response(error)

        data = {'image': file_name, 'img_hash':img_hash}
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    @staticmethod
    def get_object(img_hash):
        try:
            return Image.objects.get(img_hash=img_hash)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, img_hash, format=None):
        image = self.get_object(img_hash)
        width = self.request.query_params.get('width')
        height = self.request.query_params.get('height')
        size = self.request.query_params.get('size')
        if not width:
            width = image.image.width
        if not height:
            height = image.image.height
        if not size:
            size = image.image.size

        path = image.image.name.replace('/', '.').split('.')
        path = (f'{settings.MEDIA_URL[1:]}{settings.MEDIA_HASH_URL}{path[-2]}'
                f'_w{str(width)}_h{str(height)}_s{str(size)}.{path[-1]}')

        if os.path.isfile(path):
            img = Image_PIL.open(path)
            img_size = len(img.fp.read())
        else:
            img = Image_PIL.open(image.image.url[1:])
            img = img.resize((int(width), int(height)), Image_PIL.ANTIALIAS)
            img.save(path, quality=75)

            img = Image_PIL.open(path)
            img_size = len(img.fp.read())
            img.save(path)
            i = 75
            while img_size > int(size) and i >= 1:
                img = Image_PIL.open(path)
                img_size = len(img.fp.read())
                img.save(path, quality=i)
                i += -1

        full_url = f'{get_current_site(self.request).domain}/{path}'
        image = {'width': width, 'height': height,
                 'img_size': img_size, 'image': full_url}
        return Response(image, status=status.HTTP_200_OK)

    def delete(self, request, img_hash, format=None):
        image = self.get_object(img_hash)
        os.remove(image.image.url[1:])
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
