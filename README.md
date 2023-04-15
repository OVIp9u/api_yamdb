# YaMDB

## Описание

Яндекс практикум, проект 10 спринта.

## Что использовалось

Django, Django REST framework

## Функционал

Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число);
из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
На одно произведение пользователь может оставить только один отзыв.

### Примеры запросов

...

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/OVIp9u/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:


```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

В директории /static/data/ находится тестовая
база данных.
Для автоматического добавления тестовых записей
в базу данных запустите команду 
(также см. пункт ниже):

```
python manage.py download_data
```

Для предварительного очищения базы данных от ранее 
добавленных записей необходимо добавить дополнительный
аргумент "--delete-existing".

```
python manage.py download_data --delete-existing
```