from rest_framework import serializers

from .models import ResourceMaterial


class ResourceMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceMaterial
        fields = '__all__'
