# Generated by Django 2.0.6 on 2018-06-22 04:26

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spaceSession', '0003_step_three_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='step_five',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='pk')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='spacesession',
            name='step_five',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='spaceSession.step_five'),
            preserve_default=False,
        ),
    ]
