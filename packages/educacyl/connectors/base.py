from abc import ABC, abstractmethod
from packages.educacyl.models import ImportPackage

class OfficialConnector(ABC):
    name = "base"

    @abstractmethod
    def available(self) -> bool:
        ...

    @abstractmethod
    def import_package(self) -> ImportPackage:
        ...
