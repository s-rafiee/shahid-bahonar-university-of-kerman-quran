# Generated by Django 3.2.5 on 2021-07-24 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.IntegerField()),
                ('exporter', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('company_name', models.CharField(max_length=200)),
                ('admin_first_name', models.CharField(max_length=200)),
                ('admin_last_name', models.CharField(max_length=200)),
                ('admin_national_code', models.CharField(max_length=10)),
                ('tel', models.CharField(max_length=11)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('postal_code', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='activities/')),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.categories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
