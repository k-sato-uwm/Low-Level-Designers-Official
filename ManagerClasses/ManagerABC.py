from abc import ABC,abstractmethod
from scheduler.models import *
class AbstractManager(ABC):
    @abstractmethod
    def create(self,entry):
        pass
    @abstractmethod
    def delete(self,entry_id):
        pass
    @abstractmethod
    def update(self,entry_id,entry):
        pass
    @abstractmethod
    def view(self,entry_id):
        pass
