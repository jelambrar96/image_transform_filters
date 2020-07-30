
from abc import ABC, abstractmethod

class BasicFilter(ABC):
    @abstractmethod
    def filter(self, image):
        pass

    def config(self, config_name):
        pass


class NoneFilter(BasicFilter):
    def filter(self, image):
        return image


class CloneFilter(BasicFilter):
    def filter(self, image):
        return image.copy()
