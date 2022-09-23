class User:
    """user model
    """

    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__password = password

        return

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password
