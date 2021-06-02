from typing import List

from daos.account_dao import AccountDAO
from entities.account import Account
from utils.connection_util import connection


class AccountDAOPostgres(AccountDAO):
    def create_account(self, client_id: int) -> Account:
        sql = """insert into account values (default, %s, '', 0) returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(client_id)))
        connection.commit()
        account_id = cursor.fetchone()[0]
        account = Account(account_id, client_id, "", 0)
        return account

    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        sql = """select * from account where client_id = %s order by account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(client_id)))
        records = cursor.fetchall()
        account_list = []
        for account_parts in records:
            account = Account(account_parts[0], account_parts[1], account_parts[2], account_parts[3])
            account_list.append(account)
        return account_list

    def get_accounts_between(self, client_id: int, lower_bound: int, upper_bound: int) -> List[Account]:
        sql = """select * from account where client_id = %s and balance > %s and balance < %s order by account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(client_id), str(lower_bound), str(upper_bound)))
        records = cursor.fetchall()
        account_list = []
        for account_parts in records:
            account = Account(account_parts[0], account_parts[1], account_parts[2], account_parts[3])
            account_list.append(account)
        return account_list

    def get_account_by_account_number(self, client_id: int, account_number: int) -> Account:
        sql = """select * from account where client_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(client_id), str(account_number)))
        records = cursor.fetchall()
        for account_parts in records:
            account = Account(account_parts[0], account_parts[1], account_parts[2], account_parts[3])
            return account
        raise KeyError

    def update_account(self, client_id: int, account_number: int, account: Account) -> Account:
        sql = """update account set account_name = %s, balance = %s where client_id = %s and account_id = %s 
        returning account"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(account.name), str(account.balance), str(client_id), str(account_number)))
        connection.commit()
        return self.get_account_by_account_number(client_id, account_number)

    def deposit(self, client_id: int, account_number: int, amount: float) -> Account:
        sql = """update account set balance = balance + %s where client_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(amount), str(client_id), str(account_number)))
        connection.commit()
        return self.get_account_by_account_number(client_id, account_number)

    def withdraw(self, client_id: int, account_number: int, amount: float) -> Account:
        sql = """update account set balance = balance - %s where client_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (str(amount), str(client_id), str(account_number)))
        connection.commit()
        return self.get_account_by_account_number(client_id, account_number)

    def transfer(self, client_id: int, transfer_from: int, transfer_to: int, amount: float) -> List[Account]:
        account1 = self.withdraw(client_id, transfer_from, amount)
        account2 = self.deposit(client_id, transfer_to, amount)
        account_list = [account1, account2]
        return account_list

    def delete_account(self, client_id: int, account_number: int):
        sql = """delete from account where client_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id, account_number))
        connection.commit()
        return True
