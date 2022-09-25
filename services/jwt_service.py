import abc
from logging import Logger
from injector import inject
import base64
import json
from uuid import uuid4
from datetime import datetime, timedelta
from hashlib import sha256
import hmac
import typing as t

from core.setting import AppSettings


class JwtToken:
    def __init__(
            self, alg: t.Optional[str],
            typ: t.Optional[str],
            jti: t.Optional[str],
            iat: t.Optional[int],
            nbf: t.Optional[int],
            exp: t.Optional[int],
            sub: t.Optional[str],
            signature: t.Optional[str] = None) -> None:

        self.__alg = alg
        self.__typ = typ
        self.__jti = jti
        self.__iat = iat
        self.__nbf = nbf
        self.__exp = exp
        self.__sub = sub
        self.__signature = signature

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
    def header(self) -> dict:
        """header dict
        """

        header = {"alg": self.__alg, "typ": self.__typ}

        return header

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

    @property
    def signature(self):
        """jwt signature
        """
        return self.__signature

    @property
    def payload(self) -> dict:
        """payload dict
        """

        payload = {
            "jti": self.__jti,
            "iat": self.__iat,
            "nbf": self.__nbf,
            "exp": self.__exp,
            "sub": self.__sub,
        }

        return payload


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
        """Verify that token is correct

        Args:
            token (JwtToken): token to be verified

        Returns:
            bool: True if enabled
        """
        pass


class JwtService(IJwtService):
    """Implement of IJwtService
    """

    @inject
    def __init__(self, logger: Logger, app_settings: AppSettings) -> None:
        self.__logger = logger
        self.__app_settings = app_settings

        return

    def create_token(self, username: str) -> str:
        now = datetime.now()
        expired_at = now + timedelta(hours=1)

        jti = uuid4().hex
        iat = int(now.timestamp())
        nbf = iat
        exp = int(expired_at.timestamp())
        sub = username

        jwt_token = JwtToken(alg="HS256", typ="JWT", jti=jti, iat=iat, nbf=nbf, exp=exp, sub=sub)

        try:
            header_b64 = self.to_base64(jwt_token.header)
            payload_b64 = self.to_base64(jwt_token.payload)

            unsigned_token = f"{header_b64}.{payload_b64}"

            # https://www.w2solution.co.jp/tech/2022/08/18/flaskapi%E3%81%A7jwt%E8%AA%8D%E8%A8%BC%E3%82%92%E5%AE%9F%E8%A3%85%E3%81%99%E3%82%8B%EF%BC%88%E5%89%8D%E7%B7%A8%EF%BC%89/
            secret_key = self.__app_settings.jwt_secret.encode("utf-8")
            signature_bytes = base64.urlsafe_b64encode(hmac.new(secret_key, unsigned_token.encode("utf-8"), sha256).digest())
            signature = signature_bytes.decode("utf-8").rstrip("=")
        except Exception as e:
            self.__logger.error(f"encode jwt token error : {e}")
            raise e

        token = f"{unsigned_token}.{signature}"

        return token

    def decode_token(self, token: str) -> JwtToken:
        splited_token = token.split(".")
        if len(splited_token) < 3:
            self.__logger.error(f"invalid jwt token syntax. token: {token}")
            raise Exception("invalid jwt token syntax.")

        header_b64 = splited_token[0]
        payload_b64 = splited_token[1]
        signature = splited_token[2]

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
            signature=signature
        )

        return jwt_token

    def verify_token(self, jwt_token: JwtToken) -> bool:
        try:
            header_b64 = self.to_base64(jwt_token.header)
            payload_b64 = self.to_base64(jwt_token.payload)
            unsigned_token = f"{header_b64}.{payload_b64}"

            secret_key = self.__app_settings.jwt_secret.encode("utf-8")
            signature_bytes = base64.urlsafe_b64encode(hmac.new(secret_key, unsigned_token.encode("utf-8"), sha256).digest())
            signature = signature_bytes.decode("utf-8").rstrip("=")
        except Exception as e:
            self.__logger.error(f"encode jwt token error : {e}")
            return False

        if jwt_token.signature != signature:
            self.__logger.error(f"The signature on the jwt token is incorrect. sub: {jwt_token.sub}")
            return False

        nbf, exp = jwt_token.nbf, jwt_token.exp
        if nbf is None or exp is None:
            return False

        # The correct token should be past the start time and not expire
        enabled_at = datetime.fromtimestamp(nbf)
        expired_at = datetime.fromtimestamp(exp)
        now = datetime.now()

        if now < enabled_at:
            return False

        if now > expired_at:
            return False

        return True

    def to_base64(self, data: dict) -> str:
        """convert to JWT string from dict data
        """

        try:
            data_bytes = json.dumps(data).encode("utf-8")
            b64_data = base64.urlsafe_b64encode(data_bytes).decode("utf-8").rstrip("=")
        except Exception as e:
            self.__logger.error(f"base64 encode error : {e}")
            raise e

        return b64_data

    def to_dict(self, data: str) -> dict:
        """convert to dict data from JWT string
        """

        # Padding is added because the string length must be a multiple of 4 to decode
        data_with_padding = data + "=" * (-len(data) % 4)

        try:
            dict_str = base64.urlsafe_b64decode(data_with_padding).decode("utf-8")
            dict_data: dict = json.loads(dict_str)
        except Exception as e:
            self.__logger.error(f"dict decode error : {e}")
            raise e

        return dict_data
