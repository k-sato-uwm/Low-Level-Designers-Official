from abc import ABC,abstractmethod
from typing import Any
class AbstractManager(ABC):
    @abstractmethod
    def create(self,entry) -> None:
        pass
    @abstractmethod
    def delete(self,entry_id) -> None:
        pass
    @abstractmethod
    def update(self,entry_id,entry) -> None:
        pass
    @abstractmethod
    def view(self,entry_id) -> None:
        pass
