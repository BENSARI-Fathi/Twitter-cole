# Generated by Django 3.1.7 on 2021-04-06 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20210406_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetlike',
            name='tweet',
            field=models.ManyToManyField(blank=True, to='base.Tweet'),
        ),
    ]
