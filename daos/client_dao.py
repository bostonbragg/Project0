from abc import abstractmethod, ABC
from entities.client import Client


class ClientDAO(ABC):
    # CREATE
    @abstractmethod
    def create_client(self) -> Client:
        pass

    # READ
    @abstractmethod
    def get_client_by_id(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_all_clients(self) -> list:
        pass

    # UPDATE
    @abstractmethod
    def update_client(self, client_id: int, client: Client) -> Client:
        pass

    # DELETE
    @abstractmethod
    def delete_client(self, client_id) -> bool:
        pass
