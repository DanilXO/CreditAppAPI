# Generated by Django 2.2.7 on 2019-11-17 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='first name')),
                ('last_name', models.CharField(max_length=128, verbose_name='last name')),
                ('phone', models.CharField(max_length=16, unique=True, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='email')),
                ('passport', models.IntegerField(verbose_name='passport number')),
                ('scoring_score', models.PositiveIntegerField(verbose_name='scoring score')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('partner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'customer profile',
                'verbose_name_plural': 'customer profiles',
                'ordering': ('-created', '-updated'),
            },
        ),
        migrations.CreateModel(
            name='LoanOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('start_rotation', models.DateTimeField(verbose_name='start of rotation')),
                ('end_rotation', models.DateTimeField(verbose_name='end of rotation')),
                ('min_scoring_score', models.PositiveIntegerField(verbose_name='min scoring score')),
                ('max_scoring_score', models.PositiveIntegerField(verbose_name='max scoring score')),
                ('type', models.PositiveIntegerField(choices=[(1, 'Consumer credit'), (2, 'Mortgage'), (3, 'Car loan')], verbose_name='type')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'loan offer',
                'verbose_name_plural': 'loan offers',
                'ordering': ('-created', '-updated'),
            },
        ),
        migrations.CreateModel(
            name='LoanRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(1, 'New'), (2, 'Sent'), (3, 'Received'), (4, 'Approved'), (5, 'Denied'), (6, 'Issued')], verbose_name='status')),
                ('sent', models.DateTimeField(verbose_name='sending date')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit.CustomerProfile')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit.LoanOffer')),
            ],
            options={
                'verbose_name': 'loan request',
                'verbose_name_plural': 'loan request',
                'ordering': ('-created', '-sent'),
            },
        ),
    ]