from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import Binder, singleton
from logging import Logger, getLogger
from core.initialize import AppInitializer, IAppInitializer

from core.setting import SettingLoader, AppSettings
from core.logger import LoggerBuilder
from controllers.apis import api
from repositories.user_repos import IUserRepository, TempUserRepository
from services.weather_service import IWeatherService, WeatherService
from services.simple_token_service import ISimpleTokenService, SimpleTokenService


class AppBuilder:
    service = None

    def __init__(self) -> None:
        return

    @classmethod
    def build(self, app: Flask, cors_enable=True) -> 'AppBuilder':
        app.register_blueprint(api)

        if cors_enable:
            CORS(app=app)

        self.service = FlaskInjector(app=app, modules=[self.configure])

        return self

    @classmethod
    def configure(self, binder: Binder) -> None:
        """Configure dependency  injections
        """

        # Configure application settings
        app_settings = SettingLoader.load_setting().get_setting()

        # Setup logger
        LoggerBuilder.setup()

        binder.bind(AppSettings, to=app_settings, scope=singleton)
        binder.bind(Logger, to=getLogger("production"))
        binder.bind(IAppInitializer, to=AppInitializer)

        binder.bind(IUserRepository, to=TempUserRepository)
        binder.bind(ISimpleTokenService, to=SimpleTokenService)

        binder.bind(IWeatherService, to=WeatherService)
        return

    @classmethod
    def get_service(self) -> FlaskInjector:
        """Get service application
        """

        if not isinstance(self.service, FlaskInjector):
            raise Exception("FlaskInjector has not been built.")
        return self.service
