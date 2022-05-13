from abc import ABCMeta, abstractmethod

class queryFormattable(metaclass=ABCMeta):

    @abstractmethod
    def _formatQuery(self) -> None:
        pass



