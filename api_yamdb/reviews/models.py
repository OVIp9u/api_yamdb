from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class TitleAttribute(models.Model):
    """Абстрактная модель для атрибутов произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Category(TitleAttribute):
    """Категории произведений."""

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(TitleAttribute):
    """Жанры произведений."""

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genres',
        blank=True,
    )
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )
    year = models.IntegerField(
        blank=False,
        null=False,
    )
    description = models.TextField(
        null=True,
    )

    class Meta:
        ordering = ('name', 'year')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Связь M2M жанров и произведений."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=False,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=False,
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Модель отзывов"""
    text = models.TextField('Текст отзыва', blank=True,)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='only_one_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам"""
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

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
