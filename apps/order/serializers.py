from rest_framework import serializers

from .models import Classification, SubCategory


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = ('id', 'name', )


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'classification')
