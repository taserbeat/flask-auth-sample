import os
import pathlib
import json
import argparse

import typing as t


class AppSettings:
    FLASK_LISTEN_PORT_KEY = "FLASK_LISTEN_PORT"
    FLASK_URL_KEY = "FLASK_URL"
    FLASK_JWT_SECRET_KEY = "FLASK_JWT_SECRET"

    def __init__(self) -> None:
        self.__listen_port = 5000
        self.__url = "0.0.0.0"
        self.__jwt_secret = "my_secret_key"

        return

    def load_setting_file(self, path="settings/setting.json", path_type: t.Literal["rel", "abs"] = "rel") -> 'AppSettings':
        """Load setting from json file

        Args:
            path (str, optional): json setting file path. Defaults to "settings/setting.json".
            path_type (t.Literal[&quot;rel&quot;, &quot;abs&quot;], optional): path type. Defaults to "rel".
        """

        if path_type not in ["rel", "abs"]:
            raise Exception("value error. path_type is 'rel' or 'abs'")

        setting_file_path = path
        if path_type == "rel":
            root_dir_path = str(pathlib.Path(__file__).parent.parent)
            setting_file_path = os.path.normpath(os.path.join(root_dir_path, path))

        if not os.path.exists(setting_file_path):
            raise FileNotFoundError(f"'{setting_file_path}' is not found.")

        try:
            with open(setting_file_path, "r", encoding="utf-8") as f:
                app_settings: dict = json.load(f)
                pass
        except Exception as e:
            raise e

        # Update settings
        self.__listen_port = app_settings.get(self.FLASK_LISTEN_PORT_KEY, self.__listen_port)
        self.__url = app_settings.get(self.FLASK_URL_KEY, self.__url)
        self.__jwt_secret = app_settings.get(self.FLASK_JWT_SECRET_KEY, self.__jwt_secret)

        return self

    def load_environment(self) -> 'AppSettings':
        """
        Load setting from environment
        """

        # Update settings
        self.__listen_port = os.environ.get(self.FLASK_LISTEN_PORT_KEY, self.__listen_port)
        self.__url = os.environ.get(self.FLASK_URL_KEY, self.__url)
        self.__jwt_secret = os.environ.get(self.FLASK_JWT_SECRET_KEY, self.__jwt_secret)

        return self

    def load_cli_args(self) -> 'AppSettings':
        """
        Load setting from args
        """

        parser = argparse.ArgumentParser()

        parser.add_argument("-P", "--port", type=int, default=self.__listen_port, help="server listen port")
        parser.add_argument("-U", "--url", type=str, default=self.__url, help="server publical url address")

        args = parser.parse_args()
        arg_listen_port: int = args.port
        arg_url: str = args.url

        # Update settings
        self.__listen_port = arg_listen_port
        self.__url = arg_url

        return self

    @property
    def listen_port(self) -> int:
        """
        Server listen port
        """

        return self.__listen_port

    @property
    def url(self) -> str:
        """
        Server publical url address
        """
        return self.__url

    @property
    def jwt_secret(self) -> str:
        """
        The secret used by JWT Authentication
        """
        return self.__jwt_secret


class SettingLoader:
    app_settings = AppSettings()

    def __init__(self) -> None:
        return

    @classmethod
    def load_setting(self) -> 'SettingLoader':
        self.app_settings.load_setting_file().load_environment().load_cli_args()

        return self

    @classmethod
    def get_setting(self) -> AppSettings:
        return self.app_settings
