from rest_framework import serializers

from .models import Province, City, District, School


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    province = serializers.CharField(help_text='所属省份', label='省份',)

    class Meta:
        model = City
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    province = serializers.CharField(help_text='所属省份', label='省份', )
    city = serializers.CharField(help_text='所属市', label='市', )
    district = serializers.CharField(help_text='县/区', label='城市', )

    class Meta:
        model = District
        fields = ('id', 'province', 'city', 'district')


class DistrictInfoSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='city.province.name')
    city = serializers.CharField(source='city.name')
    district = serializers.CharField(source='name')

    class Meta:
        model = District
        fields = ('id', 'province', 'city', 'district')


class SchoolSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')
    district = serializers.CharField(source='district.name')

    class Meta:
        model = School
        fields = ('id', 'name', 'city', 'district', )


class NearestSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', 'latitude', 'longitude',)
        read_only_fields = ('id', 'name',)
