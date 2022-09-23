import abc
from logging import Logger
from injector import inject
import typing as t

from models.user import User
from repositories.user_repos import IUserRepository
from services.simple_token_service import ISimpleTokenService


class ISimpleTokenAuthorizer(metaclass=abc.ABCMeta):
    """interface of simple token authorizer
    """

    @abc.abstractmethod
    def authorize(self, token: t.Optional[str]) -> t.Optional[User]:
        pass


class SimpleTokenAuthorizer(ISimpleTokenAuthorizer):
    @inject
    def __init__(self, logger: Logger, sts: ISimpleTokenService, user_repos: IUserRepository) -> None:
        self.__logger = logger
        self.__sts = sts
        self.__user_repos = user_repos

        return

    def authorize(self, token: t.Optional[str]) -> t.Optional[User]:
        if token is None:
            self.__logger.error("token is not exist.")
            return None

        try:
            (username, password) = self.__sts.decode_token(token)
        except Exception as e:
            self.__logger.error(f"invalid token error : {str(e)}")
            return None

        try:
            user = self.__user_repos.get_first_user(username)
        except Exception as e:
            self.__logger.error(f"user repository error : {e}")
            return None

        if user is None:
            self.__logger.error(f"username: '{username}' is not exist.")
            return None

        if user.password != password:
            self.__logger.error(f"invalid token requested by username: '{username}'")
            return None

        return user


# ==========================================================================================================================
"""
TODO:
デコレータを使って認証処理を共通化したいが、APIの呼び出し側でインジェクションができない。
I want to use decorators to make the authentication process common, but cannot do injection on the API caller side.
"""

# from flask import request, Response
#
#
# def simple_token_required(controller):
#     def authorize(logger: Logger, sts: ISimpleTokenService, user_repos: IUserRepository, *args, **kwargs):
#         header_key = "Authorization"
#         simple_token = request.headers.get(header_key)

#         if simple_token is None:
#             logger.error(f"'{header_key}' is not set.")
#             return Response(status=403)

#         try:
#             (username, password) = sts.decode_token(simple_token)
#         except Exception as e:
#             logger.error(f"invalid token error : {str(e)}")
#             return Response(status=403)

#         try:
#             user = user_repos.get_first_user(username)
#         except Exception as e:
#             logger.error(f"user repository error : {e}")
#             return Response(status=403)

#         if user is None:
#             logger.error(f"username: '{username}' is not exist.")
#             return Response(status=403)

#         if user.password != password:
#             logger.error(f"invalid token requested by username: '{username}'")
#             return Response(status=403)

#         response = controller(*args, **kwargs)

#         return response

#     return authorize
