# Generated by Django 4.1.5 on 2023-02-10 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_remove_item_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('Item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item')),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.aircraft')),
            ],
        ),
    ]