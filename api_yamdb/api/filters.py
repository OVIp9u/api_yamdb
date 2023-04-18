import django_filters as df
from reviews.models import Title


class TitleFilter(df.FilterSet):
    """Фильтры для Произведений."""
    genre = df.CharFilter(
        field_name='genre__slug',
        method='filter_genre'
    )
    category = df.CharFilter(
        field_name='category__slug',
        method='filter_category'
    )
    year = df.CharFilter(
        field_name='year',
        method='filter_year'
    )
    name = df.CharFilter(
        field_name='name',
        method='filter_name'
    )

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')

    def filter_genre(self, queryset, name, genre):
        return queryset.filter(genre__slug__contains=genre)

    def filter_category(self, queryset, name, category):
        return queryset.filter(category__slug__contains=category)

    def filter_year(self, queryset, name, year):
        return queryset.filter(year__contains=year)

    def filter_name(self, queryset, name, title_name):
        return queryset.filter(name__contains=title_name)
