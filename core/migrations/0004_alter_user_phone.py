# Generated by Django 4.2 on 2025-01-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, default='unknown', help_text='لطفا شماره تلفن خود را  وارد کنید', max_length=11, null=True, unique=True),
        ),
    ]