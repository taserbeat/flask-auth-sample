import abc
from logging import Logger
from injector import inject


class IAppInitializer(metaclass=abc.ABCMeta):
    """Interface of initialize application
    """

    @abc.abstractmethod
    def initialize(self) -> None:
        """initialize logic
        """
        pass


class AppInitializer(IAppInitializer):
    """Implement initializer class
    """

    @inject
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        return

    def initialize(self) -> None:
        self.__logger.info("start initialize")

        # something to initialize...

        self.__logger.info("finish initialize")
        return
