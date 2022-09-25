import abc
from logging import Logger
from injector import inject
import base64
import json
from uuid import uuid4
from datetime import datetime, timedelta
import typing as t


class JwtToken:
    def __init__(
            self, alg: t.Optional[str],
            typ: t.Optional[str],
            jti: t.Optional[str],
            iat: t.Optional[int],
            nbf: t.Optional[int],
            exp: t.Optional[int],
            sub: t.Optional[str]) -> None:

        self.__alg = alg
        self.__typ = typ
        self.__jti = jti
        self.__iat = iat
        self.__nbf = nbf
        self.__exp = exp
        self.__sub = sub

        return

    @property
    def alg(self):
        """Algorithm
        """
        return self.__alg

    @property
    def typ(self):
        """JWT type
        """
        return self.__typ

    @property
    def jti(self):
        """Unique id of jwt token
        """
        return self.__jti

    @property
    def iat(self):
        """Unix timestamp at token created
        """
        return self.__iat

    @property
    def nbf(self):
        """Unix timestamp at token enabled
        """
        return self.__nbf

    @property
    def exp(self):
        """Unix timestamp at token expired
        """
        return self.__exp

    @property
    def sub(self):
        """Unique property that identifies the User (like username)
        """
        return self.__sub


class IJwtService(metaclass=abc.ABCMeta):
    """Interface of JWT service
    """

    @abc.abstractmethod
    def create_token(self, username: str) -> str:
        """Create JWT

        Args:
            username (str): username (unique)

        Returns:
            str: JWT
        """
        pass

    @abc.abstractmethod
    def decode_token(self, token: str) -> JwtToken:
        """Decode JWT

        Args:
            token (str): jwt token
        """
        pass

    @abc.abstractmethod
    def verify_token(self, token: JwtToken) -> bool:
        """Verify that token is enabled

        Args:
            token (JwtToken): token to be verified

        Returns:
            bool: True if enabled
        """
        pass

    @classmethod
    def to_base64(self, data: dict) -> str:
        """convert to JWT string from dict data
        """

        try:
            data_bytes = json.dumps(data).encode("utf-8")
            b64_data = base64.urlsafe_b64encode(data_bytes).decode("utf-8")
        except Exception as e:
            raise e

        return b64_data

    @classmethod
    def to_dict(self, data: str) -> dict:
        """convert to dict data from JWT string
        """

        try:
            dict_str = base64.urlsafe_b64decode(data).decode("utf-8")
            dict_data: dict = json.loads(dict_str)
            pass
        except Exception as e:
            raise e

        return dict_data


class JwtService(IJwtService):
    """Implement of IJwtService
    """

    @inject
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger

        return

    def create_token(self, username: str) -> str:
        now = datetime.now()
        expired_at = now + timedelta(hours=1)

        jti = uuid4().hex
        iat = int(now.timestamp())
        nbf = iat
        exp = int(expired_at.timestamp())
        sub = username

        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "jti": jti,
            "iat": iat,
            "nbf": nbf,
            "exp": exp,
            "sub": sub,
        }

        try:
            header_b64 = self.to_base64(header)
            payload_b64 = self.to_base64(payload)
        except Exception as e:
            self.__logger.error(f"encode jwt token error : {e}")
            raise e

        jwt_token = f"{header_b64}.{payload_b64}"

        return jwt_token

    def decode_token(self, token: str) -> JwtToken:
        splited_token = token.split(".")
        if len(splited_token) < 2:
            self.__logger.error(f"invalid jwt tokensyntax. token: {token}")
            raise Exception("invalid jwt token syntax.")

        header_b64 = splited_token[0]
        payload_b64 = splited_token[1]

        try:
            header_dict = self.to_dict(header_b64)
            payload_dict = self.to_dict(payload_b64)
        except Exception as e:
            self.__logger.error("decode jwt token error.")
            raise e

        jwt_token = JwtToken(
            alg=header_dict.get("alg"),
            typ=header_dict.get("typ"),
            jti=payload_dict.get("jti"),
            iat=payload_dict.get("iat"),
            nbf=payload_dict.get("nbf"),
            exp=payload_dict.get("exp"),
            sub=payload_dict.get("sub"),
        )

        return jwt_token

    def verify_token(self, token: JwtToken) -> bool:
        # TODO: add to verify signature

        # The enabled token should be past its start time and not past its expired time
        nbf, exp = token.nbf, token.exp
        if nbf is None or exp is None:
            return False

        enabled_at = datetime.fromtimestamp(nbf)
        expired_at = datetime.fromtimestamp(exp)
        now = datetime.now()

        if now < enabled_at:
            return False

        if now > expired_at:
            return False

        return True
