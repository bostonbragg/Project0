from entities.client import Client
from exceptions.client_not_found import ClientNotFoundError
from services.client_service_impl import ClientServiceImpl
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres

client_dao = ClientDAOPostgres
client_service = ClientServiceImpl(client_dao)


def test_check_client_validity():
    output = False
    try:
        client_service.check_client_validity(999)
    except ClientNotFoundError:
        output = True
    assert output
