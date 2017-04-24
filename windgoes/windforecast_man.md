# Windgoes

## Given a city name, find wind forecast information

### Usage:

```python
from windforecast import YahooForecastAPIHandler

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
```

### Output:

*Object:  <WindGoes. Cat: moderate breeze Lat: 51.506401 Long: -0.12721>*  
*Location:  London*  
*Country:  United Kingdom*  
*Region:   England*  
*Latitude:  51.506401*  
*Longitude:  -0.12721*  
*Wind speed:  18*  
*Wind speed category:  moderate breeze*  
*Wind cardinal direction:  north-west*  
*Wind origin in degrees:  325*  
