from flask import request, Response
from logging import Logger
from functools import wraps

from repositories.user_repos import IUserRepository
from services.simple_token_service import ISimpleTokenService


def simple_token_required(action):
    """
    Authorize user by simple token.

    Return authorized user model in **kwargs
    """

    @wraps(action)
    def authorize(*args, **kwargs):
        logger: Logger = kwargs.pop("__simple_token_required_logger")
        sts: ISimpleTokenService = kwargs.pop("__simple_token_required_sts")
        user_repos: IUserRepository = kwargs.pop("__simple_token_required_user_repos")

        header_key = "Authorization"
        simple_token = request.headers.get(header_key)

        if simple_token is None:
            logger.error(f"'{header_key}' is not set.")
            return Response(status=403)

        try:
            (username, password) = sts.decode_token(simple_token)
        except Exception as e:
            logger.error(f"invalid token error : {str(e)}")
            return Response(status=403)

        try:
            user = user_repos.get_first_user(username)
        except Exception as e:
            logger.error(f"user repository error : {e}")
            return Response(status=403)

        if user is None:
            logger.error(f"username: '{username}' is not exist.")
            return Response(status=403)

        if user.password != password:
            logger.error(f"invalid token requested by username: '{username}'")
            return Response(status=403)

        response = action(user=user, *args, **kwargs)

        return response

    # annotate injection object authorize wrapper function called
    # https://github.com/alecthomas/flask_injector/issues/52
    authorize.__annotations__["__simple_token_required_logger"] = Logger
    authorize.__annotations__["__simple_token_required_sts"] = ISimpleTokenService
    authorize.__annotations__["__simple_token_required_user_repos"] = IUserRepository

    return authorize
