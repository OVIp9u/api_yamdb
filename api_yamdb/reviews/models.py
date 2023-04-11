from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from titles.models import Title


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

    def __str__(self):
        return self.text

class Comment(models.Model):
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

    def __str__(self):
        return self.text

class Rating(models.Model):
    title = models.ForeignKey(
        Title,  on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()

    def __str__(self):
        return self.score
