# Generated by Django 2.2.3 on 2019-07-15 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SolarLevelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_level_share', models.IntegerField()),
                ('other_levels_share', models.IntegerField()),
                ('people_in_a_level', models.IntegerField()),
                ('levels', models.IntegerField()),
            ],
        ),
    ]