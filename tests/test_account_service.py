from entities.client import Client
from entities.account import Account
from exceptions.account_not_found import AccountNotFoundError
from exceptions.client_not_found import ClientNotFoundError
from exceptions.insufficient_funds import InsufficientFundsError
from services.account_service_impl import AccountServiceImpl
from services.client_service_impl import ClientServiceImpl
from daos.account_dao_local import AccountDAOLocal
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres

account_dao = AccountDAOPostgres()
client_dao = ClientDAOPostgres()
account_service = AccountServiceImpl(account_dao, client_dao)
client_service = ClientServiceImpl(client_dao)

test_account = Account(1, 1, "", 400)


def test_check_client_validity():
    output = False
    try:
        account_service.check_client_validity(999)
    except ClientNotFoundError:
        output = True
    assert output


def test_check_account_validity():
    output = False
    try:
        account_service.check_account_validity(1, 999)
    except (AccountNotFoundError, ClientNotFoundError):
        output = True
    assert output


def test_check_funds():
    account_service.create_account(1)
    output = False
    try:
        assert not account_service.check_funds(1, 6, 300)
    except InsufficientFundsError:
        output = True
    assert output
