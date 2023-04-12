from django.db import models
# from reviews.models import Rating


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        blank=False,
        null=True,
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )
    year = models.IntegerField(
        blank=False,
        null=False,
    )
    description = models.TextField()
    rating = models.CharField(
        max_length=10,
        default=None,
        blank=True,
        null=True,
    )
    # rating = models.ForeignKey(
    #     Rating,
    #     on_delete=models.SET_NULL,
    #     related_name='rating',
    #     default=None,
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
