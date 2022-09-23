import abc
import base64
from logging import Logger
import typing as t
from injector import inject


class ISimpleTokenService(metaclass=abc.ABCMeta):
    """Interface of simple token service
    """

    def create_token(self, username: str, password: str) -> str:
        """Create simple token

        Args:
            username (str): username
            password (str): raw password

        Returns:
            str: token
        """
        pass

    def decode_token(self, token: str) -> t.Tuple[str, str]:
        """Decode token

        Args:
            token (str): token

        Returns:
            t.Tuple[str, str]: (username, password)
        """
        pass


class SimpleTokenService(ISimpleTokenService):
    """Implement of ISimpleTokenService
    """

    @inject
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        return

    def create_token(self, username: str, password: str) -> str:
        token_source = "{0}:{1}".format(username, password)
        token = base64.b64encode(token_source.encode("utf-8")).decode()

        return token

    def decode_token(self, token: str) -> t.Tuple[str, str]:
        try:
            encoded_token = token.encode("utf-8")
            token_source = base64.b64decode(encoded_token).decode()

            splits = token_source.split(":", 1)

            username = splits[0]
            password = splits[1] if len(splits) == 2 else ""

        except Exception as e:
            self.__logger.error("decode token error.")
            raise e

        return (username, password)
