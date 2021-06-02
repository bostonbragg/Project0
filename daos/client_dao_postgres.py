from daos.client_dao import ClientDAO
from entities.client import Client
from utils.connection_util import connection


class ClientDAOPostgres(ClientDAO):
    def create_client(self) -> Client:
        sql = """insert into client values (default, '') returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        client_id = cursor.fetchone()[0]
        client = Client(client_id, "")
        return client

    def get_client_by_id(self, client_id: int) -> Client:
        sql = """select * from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, str(client_id))
        records = cursor.fetchall()
        for client_parts in records:
            client = Client(client_parts[0], client_parts[1])
            return client
        raise KeyError

    def get_all_clients(self) -> list:
        sql = """select * from client order by client_id"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        client_list = []

        for client_parts in records:
            client = Client(client_parts[0], client_parts[1])
            client_list.append(client)

        return client_list

    def update_client(self, client_id: int, client: Client) -> Client:
        sql = """update client set client_name = %s where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client.client_name, client_id))
        connection.commit()
        return Client(client_id, client.client_name)

    def delete_client(self, client_id) -> bool:
        sql = """delete from account where client_id = %s; delete from client where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(client_id), str(client_id)))
        connection.commit()
        return True
