from django.contrib import admin
from django import forms
from .models import SpaceSession, step_one, step_two, step_three, step_four

class SpaceSessionAdminForm(forms.ModelForm):

    class Meta:
        model = SpaceSession
        fields = '__all__'


class SpaceSessionAdmin(admin.ModelAdmin):
    form = SpaceSessionAdminForm
    list_display = ['slug', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']

admin.site.register(SpaceSession, SpaceSessionAdmin)


class step_oneAdminForm(forms.ModelForm):

    class Meta:
        model = step_one
        fields = '__all__'


class step_oneAdmin(admin.ModelAdmin):
    form = step_oneAdminForm
    list_display = ['slug', 'created', 'last_updated', 'completed']
    readonly_fields = ['slug', 'created', 'last_updated', 'completed']

admin.site.register(step_one, step_oneAdmin)


class step_twoAdminForm(forms.ModelForm):

    class Meta:
        model = step_two
        fields = '__all__'


class step_twoAdmin(admin.ModelAdmin):
    form = step_twoAdminForm
    list_display = ['slug', 'created', 'last_updated', 'completed', 'files_to_upload', 'arguments']
    readonly_fields = ['slug', 'created', 'last_updated', 'completed', 'files_to_upload', 'arguments']

admin.site.register(step_two, step_twoAdmin)


class step_threeAdminForm(forms.ModelForm):

    class Meta:
        model = step_three
        fields = '__all__'


class step_threeAdmin(admin.ModelAdmin):
    form = step_threeAdminForm
    list_display = ['slug', 'created', 'last_updated', 'completed']
    readonly_fields = ['slug', 'created', 'last_updated', 'completed']

admin.site.register(step_three, step_threeAdmin)


class step_fourAdminForm(forms.ModelForm):

    class Meta:
        model = step_four
        fields = '__all__'


class step_fourAdmin(admin.ModelAdmin):
    form = step_fourAdminForm
    list_display = ['slug', 'created', 'last_updated', 'data', 'completed']
    readonly_fields = ['slug', 'created', 'last_updated', 'data', 'completed']

admin.site.register(step_four, step_fourAdmin)


