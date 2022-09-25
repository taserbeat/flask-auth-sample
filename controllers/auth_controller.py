from flask import Blueprint, request, Response, jsonify
from logging import Logger

from repositories.user_repos import IUserRepository
from services.jwt_service import IJwtService

auth_endpoints = Blueprint("auth", __name__, url_prefix="/auth")


@auth_endpoints.route("/jwt", methods=["POST"])
def authenticate_jwt(logger: Logger, user_repos: IUserRepository, jwt_service: IJwtService):
    if "username" not in request.json or "password" not in request.json:
        return Response(status=400)

    username: str = request.json["username"]
    password: str = request.json["password"]

    user = user_repos.get_first_user(username)
    if user is None or user.password != password:
        return Response(status=400)

    try:
        jwt_token = jwt_service.create_token(username=username)
    except Exception as e:
        logger.error(f"create jwt token error : {e}")
        return Response(status=500)

    response = {
        "jwt": jwt_token,
    }

    return jsonify(response)
