import random
import typing as t


class Weather:
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    WINDY = "windy"
    RAINY = "rainy"

    def __init__(self, temperature: t.Optional[float] = None, forecast: t.Optional[str] = None) -> None:
        if temperature is None:
            temperature = round(random.uniform(0.0, 35.0), 1)
            pass

        self.__temperature = temperature

        if forecast is None:
            table = [self.SUNNY, self.CLOUDY, self.WINDY, self.RAINY]
            index = random.randint(0, len(table) - 1)
            forecast = table[index]
            pass

        self.__forecast = forecast

        return

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value: float):
        self.__temperature = value
        return

    @property
    def forecast(self):
        return self.__forecast

    @forecast.setter
    def forecast(self, value: str):
        self.__forecast = value
        return
