# Generated by Django 3.0.3 on 2020-05-10 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20200203_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]