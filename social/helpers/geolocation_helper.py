from datetime import datetime

import os
import requests
from tenacity import retry, wait_exponential
from .constants import GEO_URL, HOLIDAY_URL


class GeolocationCountriesHelper:
    """
    universal geolocation helper
    """
    def __init__(self):
        self.country_code = None

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def current_day_is_holiday(self):
        """
        checks if the present day is a holiday
        """
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        response = requests.get(
            f"{HOLIDAY_URL}/?api_key={os.getenv('HOLIDAYS_API_KEY')}"
            f"&country={self.country_code}"
            f"&year={year}&month={month}&day={day}"
        )
        return response.json()

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_location_details(self):
        response = requests.get(
            f"{GEO_URL}/?api_key={os.getenv('GEO_API_KEY')}"
        )
        data = response.json()
        self.country_code = data['country_code']
        return data
