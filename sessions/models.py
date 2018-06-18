from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields


class Session(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    step_one = models.ForeignKey(on_delete=models.CASCADE)
    step_two = models.ForeignKey(on_delete=models.CASCADE)
    step_three = models.ForeignKey(on_delete=models.CASCADE)
    step_four = models.ForeignKey(on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('sessions_session_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('sessions_session_update', args=(self.slug,))


class step_one(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    completed = models.BooleanField()


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('sessions_step_one_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('sessions_step_one_update', args=(self.slug,))


class step_two(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    completed = models.BooleanField()
    files_to_upload = JSONField(default=dict)
    arguments = JSONField(default=dict)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('sessions_step_two_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('sessions_step_two_update', args=(self.slug,))


class step_three(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    completed = models.BooleanField()


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('sessions_step_three_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('sessions_step_three_update', args=(self.slug,))


class step_four(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    data = JSONField(default=dict)
    completed = models.BooleanField()


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('sessions_step_four_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('sessions_step_four_update', args=(self.slug,))


