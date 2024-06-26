# Generated by Django 5.0.6 on 2024-05-23 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_lesson_content_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='content_url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='text_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='content_type',
            field=models.CharField(blank=True, choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')], max_length=50, null=True),
        ),
    ]
