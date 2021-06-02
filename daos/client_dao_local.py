from typing import List

from daos.client_dao import ClientDAO
from entities.client import Client


class ClientDAOLocal(ClientDAO):
    id_maker = 0
    client_table = {}

    def create_client(self) -> Client:
        self.id_maker += 1
        client_id = self.id_maker
        self.client_table[client_id] = Client(client_id, "")
        return self.client_table[client_id]

    def get_client_by_id(self, client_id: int) -> Client:
        output = self.client_table[client_id]
        return output

    def get_all_clients(self) -> List[Client]:
        client_list = list(self.client_table.values())
        return client_list

    def update_client(self, client_id: int, client: Client) -> Client:
        # replace = {client_id: client}
        # print(self.client_table[client_id])
        self.client_table[client_id] = client
        return client

    def delete_client(self, client_id) -> bool:
        del self.client_table[client_id]
        return True
