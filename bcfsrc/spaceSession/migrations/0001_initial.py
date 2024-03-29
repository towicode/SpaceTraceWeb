# Generated by Django 2.0.6 on 2018-06-21 21:12

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='pk')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='step_four',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='pk')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
                ('completed', models.BooleanField()),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='step_one',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='pk')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField()),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='step_three',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='pk')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField()),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='step_two',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='pk')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('completed', models.BooleanField()),
                ('files_to_upload', jsonfield.fields.JSONField(default=dict)),
                ('arguments', jsonfield.fields.JSONField(default=dict)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='spacesession',
            name='step_four',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaceSession.step_four'),
        ),
        migrations.AddField(
            model_name='spacesession',
            name='step_one',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaceSession.step_one'),
        ),
        migrations.AddField(
            model_name='spacesession',
            name='step_three',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaceSession.step_three'),
        ),
        migrations.AddField(
            model_name='spacesession',
            name='step_two',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spaceSession.step_two'),
        ),
    ]
