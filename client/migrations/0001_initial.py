# Generated by Django 5.0 on 2023-12-11 07:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coreapp', '0002_alter_user_dob'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('approval_status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'On Processing'), (3, 'Rejected')], default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('required_documents', models.ManyToManyField(related_name='clients_documents', to='client.documenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('approval_status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'On Processing'), (3, 'Rejected')], default=0)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('reject_reason', models.TextField(blank=True)),
                ('status', models.IntegerField(choices=[(0, 'Approve'), (1, 'reject')])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='client.client')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coreapp.document')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
