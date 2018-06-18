from . import models

from rest_framework import serializers


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Session
        fields = (
            'slug', 
            'created', 
            'last_updated', 
        )


class step_oneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.step_one
        fields = (
            'slug', 
            'created', 
            'last_updated', 
            'completed', 
        )


class step_twoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.step_two
        fields = (
            'slug', 
            'created', 
            'last_updated', 
            'completed', 
            'files_to_upload', 
            'arguments', 
        )


class step_threeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.step_three
        fields = (
            'slug', 
            'created', 
            'last_updated', 
            'completed', 
        )


class step_fourSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.step_four
        fields = (
            'slug', 
            'created', 
            'last_updated', 
            'data', 
            'completed', 
        )


