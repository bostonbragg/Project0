from abc import ABC, abstractmethod

from entities.client import Client


class ClientService(ABC):
    @abstractmethod
    def create_client(self) -> Client:
        pass

    @abstractmethod
    def get_client_by_id(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_all_clients(self) -> dict:
        pass

    @abstractmethod
    def update_client(self, client_id: int, client: Client) -> Client:
        pass

    @abstractmethod
    def delete_client(self, client_id) -> bool:
        pass

    @abstractmethod
    def check_client_validity(self, client_id: int):
        pass
