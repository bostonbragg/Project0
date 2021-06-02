from daos.client_dao import ClientDAO
from entities.client import Client
from exceptions.client_not_found import ClientNotFoundError
from services.client_service import ClientService


class ClientServiceImpl(ClientService):
    def __init__(self, client_dao: ClientDAO):
        self.client_dao: ClientDAO = client_dao

    def create_client(self) -> Client:
        return self.client_dao.create_client()

    def get_client_by_id(self, client_id: int) -> Client:
        self.check_client_validity(client_id)
        return self.client_dao.get_client_by_id(int(client_id))

    def get_all_clients(self) -> list:
        return self.client_dao.get_all_clients()

    def update_client(self, client_id: int, client: Client) -> Client:
        self.check_client_validity(client_id)
        return self.client_dao.update_client(client_id, client)

    def delete_client(self, client_id) -> bool:
        self.check_client_validity(client_id)
        return self.client_dao.delete_client(client_id)

    def check_client_validity(self, client_id: int):
        try:
            return self.client_dao.get_client_by_id(int(client_id))
        except (TypeError, KeyError, ValueError):
            raise ClientNotFoundError(f"The client with id of {client_id} does not exist.")
