from img_resizer.models import Image
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from PIL import Image as Image_PIL
import hashlib


class ImageList(APIView):

    def get(self, request, format=None):
        images = Image.objects.all()
        for image in images:
            image.image = 'http://'+get_current_site(request).domain+'/media/'+str(image.image)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,  *args, format=None,  **kwargs):
        f = request.FILES.get('file')
        path = f.name.replace('/', '.').split('.')
        name = path[-2]+'.'+path[-1]
        file_path = 'media/img/' + name
        with open(file_path, 'bw') as file:
            for chunk in f.chunks():
                file.write(chunk)
        image = 'img/' + name
        img = Image_PIL.open('media/'+image)
        img_hash = hashlib.md5(img.tobytes()).hexdigest()

        data = {'image':image, 'img_hash':img_hash}
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):

    def get_object(self, img_hash):
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
        path = 'media/img_cache/' + path[-2] + '_w' + str(width) + '_h' + str(height) + '_s' + str(size) + '.' + path[
            -1]

        img = Image_PIL.open(image.image.url[1:])
        img = img.resize((int(width), int(height)), Image_PIL.ANTIALIAS)

        img.save(path, quality=75)

        img = Image_PIL.open(path)
        img_size = len(img.fp.read())
        img.save(path)
        i = 75
        while img_size>int(size) and i>=1:
            img = Image_PIL.open(path)
            img_size = len(img.fp.read())
            img.save(path, quality=i)
            i += -1

        full_url = ''.join(['http://', get_current_site(request).domain,'/', path])

        image = {'image':full_url}

        return Response(image, status=status.HTTP_200_OK)

    def delete(self, request, img_hash, format=None):
        image = self.get_object(img_hash)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)