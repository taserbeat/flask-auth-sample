import os
import pathlib
import json
from logging import config

import typing as t


class LoggerBuilder:
    def __init__(self) -> None:
        return

    @classmethod
    def setup(self, path="settings/logger.json", path_type: t.Literal["rel", "abs"] = "rel") -> None:
        """Setup logger

        Args:
            path (str, optional): logger setting file path. Defaults to "settings/logger.json".
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
            with open(setting_file_path, 'r', encoding='utf-8') as f:
                logger_settings: dict = json.load(f)
                pass
        except Exception as e:
            raise e

        # create directory to save handler log file
        handlers: t.Dict[str, t.Dict] = logger_settings.get("handlers", {})
        for handler in handlers.values():
            log_file_path = handler.get("filename")
            if log_file_path is None:
                continue

            log_dir_name = os.path.dirname(log_file_path)
            log_dir_path = os.path.join(root_dir_path, log_dir_name)
            if not os.path.exists(log_dir_path):
                os.makedirs(log_dir_path, exist_ok=True)
                pass

        config.dictConfig(logger_settings)

        return
