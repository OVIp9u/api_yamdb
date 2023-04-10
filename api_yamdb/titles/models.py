from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


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
    rating = models.ForeignKey(
        'Rating',
        on_delete=models.SET_NULL,
        related_name='rating',
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title,  on_delete=models.CASCADE, related_name='reviews'
    )


class Comments(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )


class Rating(models.Model):
    score = models.IntegerField()

    def __str__(self):
        return self.score
