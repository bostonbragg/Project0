from daos.account_dao_local import AccountDAOLocal
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.account import Account
from utils.connection_util import connection

try:
    sql = """drop table account;
    drop table client;
    create table client(
        client_id int primary key generated always as identity,
        client_name varchar(50)
    );
    create table account(
        account_id int primary key generated always as identity,
        client_id int,
        account_name varchar(50),
        balance int,
        constraint fk_cl_ac foreign key (client_id) references client(client_id)
    );"""
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
except Exception as e:
    print("Database not detected")

account_dao = AccountDAOPostgres()
client_dao = ClientDAOPostgres()
test_account = Account(2, 1, "", 0)
client_dao.create_client()
client_dao.create_client()
client_dao.create_client()
client_dao.create_client()
account_dao.create_account(3)
account_dao.create_account(3)
account_dao.create_account(3)


def test_create_account():
    output = account_dao.create_account(3)
    assert output.account_id != 0


def test_get_accounts_by_client_id():
    client_id = 3
    output = account_dao.get_accounts_by_client_id(client_id)
    assert output[0].client_id == client_id


def test_get_accounts_between():
    test_account1 = Account(2, 3, "", 20)
    test_account2 = Account(3, 3, "", 90)

    account_dao.create_account(3)
    account_dao.create_account(3)
    account_dao.create_account(3)

    account_dao.update_account(3, 2, test_account1)
    account_dao.update_account(3, 3, test_account2)

    test_output = account_dao.get_accounts_between(3, 10, 100)
    desired_output = [test_account1, test_account2]
    assert test_output[0].balance == desired_output[0].balance


def test_get_account_by_account_number():
    test_output = account_dao.update_account(3, 1, Account(1, 3, "", 0))
    assert test_output.account_id == 1


def test_update_account():
    test_output = Account(1, 3, "test", 500)
    account_dao.update_account(3, 1, test_output)
    desired_output = account_dao.get_account_by_account_number(3, 1)
    assert test_output.balance == desired_output.balance


def test_deposit():
    desired_output = Account(1, 3, "", 500)
    account_before = Account(1, 3, "", 0)

    account_dao.update_account(3, 1, account_before)
    test_output = account_dao.deposit(3, 1, 500)

    assert test_output.balance == desired_output.balance


def test_withdraw():
    desired_output = Account(1, 3, "", 10)
    account_before = Account(1, 3, "", 100)

    account_dao.update_account(3, 1, account_before)
    test_output = account_dao.withdraw(3, 1, 90)

    assert test_output.balance == desired_output.balance


def test_transfer():
    account_1_before = Account(1, 3, "", 200)
    account_2_before = Account(2, 3, "", 400)
    desired_output_1 = Account(1, 3, "", 100)
    desired_output_2 = Account(2, 3, "", 500)

    account_dao.create_account(3)

    account_dao.update_account(3, 1, account_1_before)
    account_dao.update_account(3, 2, account_2_before)

    account_dao.transfer(3, 1, 2, 100)
    test_output_1 = account_dao.get_account_by_account_number(3, 1)
    test_output_2 = account_dao.get_account_by_account_number(3, 2)
    assert test_output_1.balance == desired_output_1.balance


def test_delete_account():
    assert account_dao.delete_account(3, 3)

try:
    sql = """drop table account;
    drop table client;
    create table client(
        client_id int primary key generated always as identity,
        client_name varchar(50)
    );
    create table account(
        account_id int primary key generated always as identity,
        client_id int,
        account_name varchar(50),
        balance int,
        constraint fk_cl_ac foreign key (client_id) references client(client_id)
    );"""
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
except Exception as e:
    print("Database not detected")
