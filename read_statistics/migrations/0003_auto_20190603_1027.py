# Generated by Django 2.0 on 2019-06-03 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0002_readdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='readnum',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
