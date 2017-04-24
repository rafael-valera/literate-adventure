# /usr/bin/python3

"""
    Given a city name, find wind forecast information

    Copyright (C) 2017 rafael valera

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import requests


class DirectionParser:
    """ Parses degrees to Cardinal, Ordinal or Secondary-Intercardinal directions """

    directions = {
        "north_w": {"base": 348.75, "top": 360, "cardinal": "north"},
        "north_e": {"base": 0, "top": 11.25, "cardinal": "north"},
        "north_north_east": {"base": 11.25, "top": 33.75, "cardinal": "north-north-east"},
        "north_east": {"base": 33.75, "top": 56.25, "cardinal": "north-east"},
        "east_north_east": {"base": 56.25, "top": 78.75, "cardinal": "east-north-east"},
        "east": {"base": 78.75, "top": 101.25, "cardinal": "east"},
        "east_south_east": {"base": 101.25, "top": 123.75, "cardinal": "east-south-east"},
        "south_east": {"base": 123.75, "top": 146.25, "cardinal": "south-east"},
        "south_south_east": {"base": 146.25, "top": 168.75, "cardinal": "south-south-east"},
        "south": {"base": 168.75, "top": 191.25, "cardinal": "south"},
        "south_south_west": {"base": 191.25, "top": 213.75, "cardinal": "south-south-west"},
        "south_west": {"base": 213.75, "top": 236.25, "cardinal": "south-west"},
        "west_south_west": {"base": 236.25, "top": 258.75, "cardinal": "west-south-west"},
        "west": {"base": 258.75, "top": 281.25, "cardinal": "west"},
        "west_north_west": {"base": 281.25, "top": 303.75, "cardinal": "west-north-west"},
        "north_west": {"base": 303.75, "top": 326.25, "cardinal": "north-west"},
        "north_north_west": {"base": 362.25, "top": 348.75, "cardinal": "north-north-west"},
    }

    @classmethod
    def get_direction(cls, degrees):
        """ Takes a degrees argument as wind origin and returns a string of a cardinal,
        ordinal or secondary-intercardinal direction """
        for val in cls.directions.values():
            if val.get("base") <= degrees <= val.get("top"):
                return val.get("cardinal")


class BeaufortScaleParser:
    """ Parses wind's speed into Beaufort scale wind speed definition """

    scale = [
        {"calm": {"level": 0, "base_speed": 0, "top_speed": 1}},
        {"light air": {"level": 1, "base_speed": 1, "top_speed": 3}},
        {"light breeze": {"level": 2, "base_speed": 4, "top_speed": 7}},
        {"gentle breeze": {"level": 3, "base_speed": 8, "top_speed": 12}},
        {"moderate breeze": {"level": 4, "base_speed": 13, "top_speed": 18}},
        {"fresh breeze": {"level": 5, "base_speed": 19, "top_speed": 24}},
        {"strong breeze": {"level": 6, "base_speed": 25, "top_speed": 31}},
        {"high wind": {"level": 7, "base_speed": 32, "top_speed": 38}},
        {"gale": {"level": 8, "base_speed": 39, "top_speed": 46}},
        {"strong gale": {"level": 9, "base_speed": 47, "top_speed": 54}},
        {"storm": {"level": 10, "base_speed": 55, "top_speed": 63}},
        {"violent storm": {"level": 11, "base_speed": 64, "top_speed": 72}},
        {"hurricane": {"level": 12, "base_speed": 73, "top_speed": 1000}},
        {"calm": {"level": 1, "base_speed": 0, "top_speed": 1}}
    ]

    @classmethod
    def get_wind_category(cls, wind_speed):
        """ Takes wind's speed as argument and returns a string of its definition
         in the Beaufort scale """
        for value in cls.scale:
            for k, v in value.items():
                if v.get("top_speed") >= wind_speed >= v.get("base_speed"):
                    return k


class CityNotFound(Exception):
    """ Raised when a city is not found """

    def __init__(self, *args, **kwargs):
        self.message = args[0]
        Exception.__init__(self, args, kwargs)

    def __str__(self):
        return self.message


class WindForecast:
    """ Wind forecast object """

    def __init__(self, **kwargs):
        accepted_args = ["location", "region", "latitude", "longitude", "beaufort",
                         "speed", "origin", "country", "degrees", "direction"]
        for arg in kwargs.keys():
            if arg in accepted_args:
                self.__setattr__(arg, kwargs.get(arg))

    def __str__(self):
        return "<WindGoes. Cat: {} Lat: {} Long: {}>".format(self.beaufort, self.latitude, self.longitude)


class YahooForecastAPIHandler:
    """ Retrieves forecast information from Yahoo Forecast API """

    wind_forecast_url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather." \
                        "forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20" \
                        "where%20text%3D%22{cityname}%2C%20be%22)&format=json&env=store%3A%2F" \
                        "%2Fdatatables.org%2Falltableswithkeys"

    @staticmethod
    def __request(url):
        """ Executes a GET http request, parses json string and returns a dictionary """
        response = requests.get(url).text
        data = json.loads(response)
        return data

    @classmethod
    def get_wind_forecast(cls, location):
        """ Requests wind information to yahoo forecast api, parses json, returns WindForecast object """
        parsed_json = cls.__request(cls.wind_forecast_url.format(cityname=location))
        data = parsed_json.get("query").get("results")
        if data:
            global_data = data.get("channel")
            wind_forecast_data = global_data.get("wind")
            wind_speed = int(wind_forecast_data.get("speed"))
            degrees = int(wind_forecast_data.get("direction"))
            full_location = global_data.get("location")
            latitude = global_data.get("item").get("lat")
            longitude = global_data.get("item").get("long")

            wind_forecast = dict(
                location=location,
                speed=wind_speed,
                direction=DirectionParser.get_direction(degrees),
                region=full_location.get("region"),
                latitude=latitude,
                longitude=longitude,
                degrees=degrees,
                country=full_location.get("country"),
                beaufort=BeaufortScaleParser.get_wind_category(wind_speed),
                origin=DirectionParser.get_direction(degrees)
            )
            return WindForecast(**wind_forecast)
        else:
            raise CityNotFound("{} was not found".format(location))


def main():
    wind_forecast_london = YahooForecastAPIHandler.get_wind_forecast("London")

    print("Object: ", wind_forecast_london)

    # geographic data
    print("Location: ", wind_forecast_london.location)
    print("Country: ", wind_forecast_london.country)
    print("Region: ", wind_forecast_london.region)
    print("Latitude: ", wind_forecast_london.latitude)
    print("Longitude: ", wind_forecast_london.longitude)

    # wind forecast data
    print("Wind speed: ", wind_forecast_london.speed)
    print("Wind speed category: ", wind_forecast_london.beaufort)
    print("Wind cardinal direction: ", wind_forecast_london.direction)
    print("Wind origin in degrees: ", wind_forecast_london.degrees)


if __name__ == "__main__":
    main()
