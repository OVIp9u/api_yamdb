# Generated by Django 3.2 on 2023-04-13 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20230410_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='titles.category'),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='titles.genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='titles.title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='titles.GenreTitle', to='titles.Genre'),
        ),
    ]
