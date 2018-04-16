from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Province, City, Country
from .serializers import CountrySerializer


class CountryViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountrySerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.data
        province_name = rec_dict['province']
        city_name = rec_dict['city']
        country_name = rec_dict['country']

        province_clean_name = Province.clear_name(province_name)
        city_clean_name = City.clear_name(city_name)
        country_clean_name = Country.clear_name(country_name)

        province_instance = Province.objects.filter(Q(name=province_name) | Q(name=province_clean_name))
        if province_instance.count():
            province = province_instance[0]
            rec_dict['province_id'] = province.id

            city_instance = City.objects.filter(Q(name=city_name) | Q(name=city_clean_name))
            if city_instance.count():
                city = city_instance[0]
                rec_dict['city_id'] = city.id

                country_instance = Country.objects.filter(Q(name=country_name) | Q(name=country_clean_name))
                if country_instance.count():
                    country = country_instance[0]
                    rec_dict['country_id'] = country.id
                    return Response(rec_dict, status.HTTP_200_OK)
                else:
                    country = Country.objects.create(name=country_clean_name, city=city)
                    rec_dict['country_id'] = country.id
                    return Response(rec_dict, status.HTTP_201_CREATED)
            else:
                city = City.objects.create(name=city_clean_name, province=province)
                rec_dict['city_id'] = city.id
                country = Country.objects.create(name=country_clean_name, city=city)
                rec_dict['country_id'] = country.id
                return Response({}, status.HTTP_201_CREATED)
        else:
            province = Province.objects.create(name=province_clean_name)
            city = City.objects.create(name=city_clean_name, province=province)
            country = Country.objects.create(name=country_clean_name, city=city)

            rec_dict['city_id'] = city.id
            rec_dict['country_id'] = country.id
            rec_dict['province_id'] = province.id

            return Response(rec_dict, status.HTTP_201_CREATED)
