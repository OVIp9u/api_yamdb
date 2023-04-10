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
        blank=True,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genres',
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    # rating = models.ForeignKey(
    #     'Rating',
    #     on_delete=models.SET_NULL,
    #     related_name='rating',
    #     default=None,
    #     blank=True,
    #     null=True,
    # )

    def __str__(self):
        return self.name
