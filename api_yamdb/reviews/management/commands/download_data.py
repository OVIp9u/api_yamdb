import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

OBJECTS_LIST = {
    'Произведения': Title,
    'Жанры': Genre,
    'Категории': Category,
    'Отзывы': Review,
    'Комментарии': Comment,
    'Жанры_Произведения': GenreTitle,
    'Пользователи': User,
}


def clear_data(self):
    for key, value in OBJECTS_LIST.items():
        value.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                f'Существующие записи "{key}" были удалены.'
            )
        )


class Command(BaseCommand):
    help = "Загружает CSV данные из файла data."

    def add_arguments(self, parser):
        # Аргумент для удаления всех имеющихся в БД данных
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Удаляет существующие данные, записанные ранее',
        )

    def handle(self, *args, **options):
        """Загрузка Категорий."""

        if options["delete_existing"]:
            clear_data(self)

        records = []
        with open(
            'static/data/category.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Category(
                    id=row['id'], name=row['name'], slug=row['slug']
                )
                records.append(record)

        Category.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Категорий" сохранены')
        )

        """Загрузка Жанров."""
        records = []
        with open(
            'static/data/genre.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Genre(
                    id=row['id'], name=row['name'], slug=row['slug']
                )
                records.append(record)

        Genre.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Жанров" сохранены')
        )

        """Загрузка Произведений."""
        records = []
        with open(
            'static/data/titles.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )
                records.append(record)

        Title.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Произведений" сохранены')
        )

        """Загрузка связанной таблицы Жанры-Произведения."""
        records = []
        with open(
            'static/data/genre_title.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                records.append(record)

        GenreTitle.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Жанров-Произведений" сохранены')
        )

        """Загрузка Пользователей."""
        records = []
        with open(
            'static/data/users.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                records.append(record)

        User.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Пользователей" сохранены')
        )

        """Загрузка Отзывов."""
        records = []
        with open(
            'static/data/review.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                records.append(record)

        Review.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Отзывов" сохранены')
        )

        """Загрузка Комментариев."""
        records = []
        with open(
            'static/data/comments.csv', encoding='utf-8', newline=''
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                record = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )
                records.append(record)

        Comment.objects.bulk_create(records)
        self.stdout.write(
            self.style.SUCCESS('Все записи "Комментариев" сохранены')
        )
