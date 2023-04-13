# Generated by Django 3.2 on 2023-04-13 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0005_auto_20230413_1241'),
        ('reviews', '0002_rename_comments_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='title',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rev', to='titles.title'),
            preserve_default=False,
        ),
    ]
