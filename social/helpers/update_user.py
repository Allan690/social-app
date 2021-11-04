from django.shortcuts import get_object_or_404
from django.db import connection
from ..authentication.models import User
from ..helpers.geolocation_helper import GeolocationCountriesHelper

import threading


class UpdateUserThread(threading.Thread):
    def __init__(self, email, **kwargs):
        self.user = email
        super(UpdateUserThread, self).__init__(**kwargs)

    def run(self):
        user = get_object_or_404(User, email=self.user)
        geo = GeolocationCountriesHelper()
        user.geolocation_data = geo.get_location_details()
        user.signup_date_holiday = geo.current_day_is_holiday()
        user.save()
        connection.close()
