from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)

admin.site.register(Category)

admin.site.register(Genre)

admin.site.register(GenreTitle)
