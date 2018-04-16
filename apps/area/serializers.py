from rest_framework import serializers

from .models import Province, City, Country


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    province = serializers.CharField(help_text='所属省份', label='省份',)

    class Meta:
        model = City
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    province = serializers.CharField(help_text='所属省份', label='省份', )
    city = serializers.CharField(help_text='所属市', label='市', )
    country = serializers.CharField(help_text='县/区', label='城市', )

    class Meta:
        model = Country
        fields = ('id', 'province', 'city', 'country')
