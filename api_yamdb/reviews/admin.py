from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)

admin.site.register(Category)

admin.site.register(Genre)

admin.site.register(GenreTitle)

admin.site.register(Review)

admin.site.register(Comment)
