from rest_framework import serializers

from .models import Province, City, District, School, Address


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    province = serializers.CharField(help_text='所属省份', label='省份',)

    class Meta:
        model = City
        fields = '__all__'


class CityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'

    def validate(self, attrs):
        pass


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')


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
    district = serializers.CharField(source='district.name')
    # city = serializers.CharField(source='name')

    class Meta:
        model = School
        fields = ('id', 'name', 'district', 'first_pinyin')
        # fields = ('id', 'city', 'pinyin', 'first_pinyin')


class NearestSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('id', 'name', 'latitude', 'longitude',)
        read_only_fields = ('id', 'name',)


class AddressInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class AddressShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'name', 'detail', 'user')


class AddressCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Address
        fields = ('id', 'name', 'detail', 'latitude', 'longitude', 'district', 'user')
        read_only_fields = ('id',)

