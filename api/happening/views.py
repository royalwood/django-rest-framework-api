import math
from django.db.models import Q
from datetime import datetime, date, timedelta
import calendar

from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from groups.models import Event, StudentServiceDropin
from groups.serializers import (
    EventSerializer, HappeningStudentServiceDropinSerializer)


class HappeningView(views.APIView):
    """
    A read-only endpoint. Any authenticated user can see the info.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): #pylint:disable=redefined-builtin

        result = {}

        user = self.request.user
        campus = self.request.query_params.get('campus')
        course = self.request.query_params.get('course')
        on_campus = self.request.query_params.get('on_campus')
        distance_nearby = self.request.query_params.get('distance')

        near_by_users = get_user_model().objects
        near_by_users = near_by_users.filter(groups=2, uni=self.request.user.uni)
        near_by_users = near_by_users.exclude(user=self.request.user)
        near_by_users = near_by_users.order_by('last_name')

        if campus:
            near_by_users = near_by_users.filter(campus=campus)
        if course:
            near_by_users = near_by_users.filter(course=course)
        if on_campus:
            users_campus = user.campus

            if user.campus.longitude and user.campus.latitude:

                lat = float(user.campus.latitude)
                lon = float(user.campus.longitude)

                earth_radius = 6378.1  # earth radius
                # distance in km
                if distance_nearby:
                    distance = float(distance_nearby)
                else:
                    distance = 5.0

                lat1 = lat - math.degrees(distance / earth_radius)
                lat2 = lat + math.degrees(distance / earth_radius)
                long1 = lon - math.degrees(distance / earth_radius / math.cos(math.degrees(lat)))
                long2 = lon + math.degrees(distance / earth_radius / math.cos(math.degrees(lat)))

                near_by_users = near_by_users.filter(campus=users_campus).filter(latitude__gte=lat1, latitude__lte=lat2)\
                    .filter(longitude__gte=long1, longitude__lte=long2)
            else:
                near_by_users = []
        # else:
        #     near_by_users = []

        context={'auth_user': self.request.user}
        serializer = UserSerializer(near_by_users, many=True, context=context)
        result["users"] = serializer.data

        recent_events = Event.objects.all().filter(Q(start_date__gte=datetime.now()) | Q(end_date__gte=datetime.now())).order_by('start_date')[:3]
        result["events"] = EventSerializer(recent_events, many=True).data


        today = date.today()
        tomorrow = today + timedelta(days=1)
        current_day = calendar.day_name[today.weekday()]
        tomorrow_day = calendar.day_name[tomorrow.weekday()]

        query_today = StudentServiceDropin.objects.all().filter(dropin_day__icontains=current_day).order_by('dropin_start')[:1]
        query_tomorrow = StudentServiceDropin.objects.all().filter(dropin_day__icontains=tomorrow_day).order_by('dropin_start')[:1]

        result["consultants"] = {}

        if query_today.exists():
            result["consultants"] = HappeningStudentServiceDropinSerializer(query_today[0]).data
        elif query_tomorrow.exists():
            result["consultants"] = HappeningStudentServiceDropinSerializer(query_tomorrow[0]).data

        return Response(result)
