from ManagerABC import AbstractManager

class LabManager(AbstractManager):
    @staticmethod
    def create(entry: dict) -> bool:
        pass

    def view(lab_id: int) -> dict:
        pass

    def update(lab_id: int, entry: dict) -> bool:
        pass

    def delete(lab_id: int) -> bool:
        pass