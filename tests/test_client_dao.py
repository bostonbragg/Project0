from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from utils.connection_util import connection

client_dao = ClientDAOPostgres()
test_client = Client(client_id=3, client_name="Jane Doe")
client_dao.create_client()
client_dao.create_client()
client_dao.create_client()
client_dao.create_client()


def test_create_client():
    assert client_dao.get_all_clients() != [] and client_dao.get_all_clients()[0] != 0


def test_get_client_by_id():
    client = client_dao.get_client_by_id(3)
    assert client.client_id == 3


def test_get_all_clients():
    client_dao.create_client()
    client_dao.create_client()
    client_dao.create_client()
    assert len(client_dao.get_all_clients()) >= 3


def test_update_client():
    updated_client = client_dao.update_client(client_id=test_client.client_id, client=test_client)
    assert test_client.client_name == updated_client.client_name and test_client.client_id == updated_client.client_id


def test_delete_client():
    assert client_dao.delete_client(test_client.client_id)
    try:
        d = client_dao.get_client_by_id(test_client.client_id)
    except KeyError:
        assert True
