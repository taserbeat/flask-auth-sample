import abc
import typing as t

from models.weather import Weather


class IWeatherService(metaclass=abc.ABCMeta):
    """Interface of Weather Service
    """

    @abc.abstractmethod
    def create_weather(self) -> Weather:
        """Create a weather data

        Returns:
            Weather: Weather model
        """
        pass

    @abc.abstractmethod
    def create_weathers(self, count: int) -> t.List[Weather]:
        """Create weather datas

        Args:
            count (int): count of created datas

        Returns:
            t.List[Weather]: Weather model list
        """
        pass


class WeatherService(IWeatherService):
    """Implement IWeatherService interface
    """

    def create_weather(self) -> Weather:
        weather = Weather()
        return weather

    def create_weathers(self, count: int) -> t.List[Weather]:
        weathers: t.List[Weather] = []
        for _ in range(count):
            weather = Weather()
            weathers.append(weather)

        return weathers


class WeatherServiceSimple(IWeatherService):
    """another implement
    """

    def create_weather(self) -> Weather:
        weather = Weather(temperature=54.3, forecast="nice")
        return weather

    def create_weathers(self, count: int) -> t.List[Weather]:
        weathers: t.List[Weather] = []
        for _ in range(count):
            weather = Weather(temperature=54.3, forecast="nice")
            weathers.append(weather)

        return weathers
