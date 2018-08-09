from django.db.models import Q
from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Province, City, District, School
from .serializers import DistrictSerializer, SchoolSerializer, NearestSchoolSerializer
from utils.common import response_data_group


class DistrictViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = DistrictSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.data
        province_name = rec_dict['province']
        city_name = rec_dict['city']
        district_name = rec_dict['district']

        province_clean_name = Province.clear_name(province_name)
        city_clean_name = City.clear_name(city_name)
        district_clean_name = District.clear_name(district_name)

        province_instance = Province.objects.filter(Q(name=province_name) | Q(name=province_clean_name))
        if province_instance.count():
            province = province_instance[0]
            rec_dict['province_id'] = province.id

            city_instance = City.objects.filter(Q(name=city_name) | Q(name=city_clean_name))
            if city_instance.count():
                city = city_instance[0]
                rec_dict['city_id'] = city.id

                district_instance = District.objects.filter(Q(name=district_name) | Q(name=district_clean_name))
                if district_instance.count():
                    district = district_instance[0]
                    rec_dict['district_id'] = district.id
                    return Response(rec_dict, status.HTTP_200_OK)
                else:
                    district = District.objects.create(name=district_clean_name, city=city)
                    rec_dict['district_id'] = district.id
                    return Response(rec_dict, status.HTTP_201_CREATED)
            else:
                city = City.objects.create(name=city_clean_name, province=province)
                rec_dict['city_id'] = city.id
                district = District.objects.create(name=district_clean_name, city=city)
                rec_dict['district_id'] = district.id
                return Response({}, status.HTTP_201_CREATED)
        else:
            province = Province.objects.create(name=province_clean_name)
            city = City.objects.create(name=city_clean_name, province=province)
            district = District.objects.create(name=district_clean_name, city=city)

            rec_dict['province_id'] = province.id
            rec_dict['city_id'] = city.id
            rec_dict['district_id'] = district.id

            return Response(rec_dict, status.HTTP_201_CREATED)


class SchoolViewSet(ListModelMixin, viewsets.GenericViewSet):
    """学校相关接口
    list:
        所有学校列表
    """
    queryset = School.objects.filter(is_active=True)
    authentication_classes = (JSONWebTokenAuthentication, )

    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'list':
            return SchoolSerializer
        elif self.action == 'nearest':
            return NearestSchoolSerializer
        return SchoolSerializer

    def list(self, request, *args, **kwargs):
        response = super(SchoolViewSet, self).list(request, *args, **kwargs)
        # 下面的是做了分组
        response.data = response_data_group(response.data, 'first_pinyin')
        return response


    @action(methods=['post'], detail=False)
    def nearest(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.data
        now_geohash = School.get_geohash(lat=rec_dict.get('latitude'), lon=rec_dict.get('longitude'), deep=6)
        for length in range(6, 3, -1):
            geohash_str = now_geohash[0:length]
            near_schools = School.objects.filter(geohash__startswith=geohash_str)
            if near_schools.count() > 0:
                near_school = near_schools.first()
                serializer = SchoolSerializer(near_school)
                return Response(serializer.data)
        return Response({'msg': '未定位到最近的学校'}, status=status.HTTP_401_UNAUTHORIZED)