import abc
import typing as t

from models.user import User


class IUserRepository(metaclass=abc.ABCMeta):
    """User repository interface (database client)
    """

    @abc.abstractmethod
    def get_first_user(self, username: str) -> t.Optional[User]:
        """Get user data from repository

        Args:
            username (str): unique name of user

        Returns:
            t.Optional[User]: user model or None
        """
        pass


class TempUserRepository(IUserRepository):
    """Temporary user repository
    """

    temp_users = [
        # curl <url> -H "Authorization:YWRtaW46YWRtaW4="
        User(username="admin", password="admin"),

        # curl <url> -H "Authorization:ZXhhbXBsZTp0ZW1w"
        User(username="example", password="temp")
    ]

    def __init__(self) -> None:
        return

    def get_first_user(self, username: str) -> t.Optional[User]:
        for user in self.temp_users:
            if username == user.username:
                return user

        return None
