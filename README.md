# Image resize service

Небольшое приложение для загрузки, изменения размера и качества изображений. Приложение написано на языке Python с использованием Django.

# Используемые технологии

+ Python 3.7
+ Django 2.1.3
+ Django REST Framework 3.9.2
+ Pillow 6.0.0
+ SQLite

## Приложение включает в себя следующие страницы:

1. Страница просмотра загруженных изображений.

2.	Страница загрузки изображений из файла или по ссылке, содержит форму с двумя полями: 
    + Загрузка из файла
    + Загрузка по ссылке

3.	Страница изображения содержит само изображение и форму с тремя полями:
    + Width
    + Height 
    + Size 
Принимает от нуля до трёх агрументов и выводит обработанное изображение с изменёнными значениями ширины, высоты и/или качества. Так как обработка изображения производится средствами модуля Pillow (PIL), то градация изменения веса - качества ограничена параметром quality.

# API
Реализованы методы REST API для загрузки и обработки изображений по средствам api.
1. Метод возвращает ссылки на изображения и их md5.
    ```python
    requests.get('http://localhost:8000/api_v1/images/')
    ```
2. Метод позволяет указать какое именно изображения и как изменить. Параметры не обязательные, могут присутствовать как все так и ни одного. Возвращет ссылку на изображение.
    В параметре hash указывается md5 из списка загруженных изображений, в int указывается ширины, высота и максимальный размер в байтах.
    ```python
    requests.get('http://localhost:8000/api_v1/images/<hash>', params={'width':<int>, 'height':<int>, 'size':<int>}
    ```
3. Метод загрузки изображения.
    Параметр path to image принимает путь к файлу.
    ```python
    requests.post('http://localhost:8000/api_v1/images/', files={'file': open(<path to image>, 'br')})
    ```
    Так же мозжно загружать изображение через ссылку. Параметр URL принимет ссылку на изображение.
    ```python
    requests.post('http://localhost:8000/api_v1/images/', data={'url': <url>})
    ```
4. Метод удаления заявки.
    В параметре hash указывается md5 загруженного изображения.
    ```python
    requests.delete('http://localhost:8000/snippets/<hash>')
    ```
    
    # Процес локального запуска приложения
Для локального запуска приложения созданы идентичные скрипты start.bat и start.sh. Они выполлняют следующие команды:
+ pip install -r requirements.txt - установка пакетов необходимых для работы приложения.
+ python manage.py makemigrations - проверка изменения модели в приложении (опционально, да).
+ python manage.py migrate - создание базы данных и запись в неё модели приложения.
+ python manage.py createcachetable - создание в базе данных таблицы для хранения хэша.
+ python manage.py runserver - запус самого приложения (по умолчанию localhost:8000)

# Описание деплоя приложения
    Своими словами
Вначале нужно залить проект на github. Развернуть виртуальную среду на сервере, хотя это от человека зависит или от сервера. Скачать проект с github. Обновить gitignore, settings.py перевести DEBUG в значени False, обновить SECRET_KEY, указать ALLOWED_HOSTS, настроить статику, создать базу данных. Запустить приложение.
