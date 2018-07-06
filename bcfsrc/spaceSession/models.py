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
from jsonfield import JSONField


class SpaceSession(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='pk', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    step_one = models.ForeignKey('step_one', on_delete=models.CASCADE)
    step_two = models.ForeignKey('step_two', on_delete=models.CASCADE)
    step_three = models.ForeignKey('step_three', on_delete=models.CASCADE)
    step_four = models.ForeignKey('step_four', on_delete=models.CASCADE)
    step_five = models.ForeignKey('step_five', on_delete=models.CASCADE)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('spaceSession_spaceSession_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('spaceSession_spaceSession_update', args=(self.slug,))


class step_one(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='pk', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    completed = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('spaceSession_step_one_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('spaceSession_step_one_update', args=(self.slug,))


class step_two(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='pk', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    completed = models.BooleanField(default=False)
    files_to_upload = JSONField(default=dict)
    arguments = JSONField(default=dict)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('spaceSession_step_two_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('spaceSession_step_two_update', args=(self.slug,))


class step_three(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='pk', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    data = JSONField(default=dict)
    completed = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('spaceSession_step_three_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('spaceSession_step_three_update', args=(self.slug,))


class step_four(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='pk', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    data = JSONField(default=dict)
    completed = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('spaceSession_step_four_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('spaceSession_step_four_update', args=(self.slug,))

class step_five(models.Model):

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='pk', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    data = JSONField(default=dict)
    completed = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('spaceSession_step_five_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('spaceSession_step_five_update', args=(self.slug,))


