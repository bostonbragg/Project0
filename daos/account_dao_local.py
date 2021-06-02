from typing import List

from daos.account_dao import AccountDAO
from entities.account import Account

number_maker = {}
account_table = {}


class AccountDAOLocal(AccountDAO):

    def create_account(self, client_id: int) -> Account:
        if client_id not in number_maker:
            number_maker[client_id] = 1
        else:
            number_maker[client_id] += 1

        account = Account(number_maker[client_id], client_id, "", 0)

        if client_id not in account_table:
            account_table[client_id] = list()

        account_table[client_id].append(account)

        return account

    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        return account_table[client_id]

    def get_accounts_between(self, client_id: int, lower_bound: int, upper_bound: int) -> List[Account]:
        all_client_accounts = self.get_accounts_by_client_id(client_id)
        output = list()

        for account in all_client_accounts:
            if upper_bound > account.balance > lower_bound:
                output.append(account)

        return output

    def get_account_by_account_number(self, client_id: int, account_number: int) -> Account:
        all_client_accounts = self.get_accounts_by_client_id(client_id)

        for account in all_client_accounts:
            if account.account_id == account_number:
                return account
        raise KeyError

    def update_account(self, client_id: int, account_number: int, account: Account) -> Account:
        for index, item in enumerate(account_table[client_id]):
            if item.account_id == account_number:
                account_table[client_id][index] = account

        return self.get_account_by_account_number(client_id, account_number)

    def delete_account(self, client_id: int, account_number: int):
        for index, item in enumerate(account_table[client_id]):
            if item.account_id == account_number:
                del account_table[client_id][index]
                return True
        raise KeyError

    def deposit(self, client_id: int, account_number: int, amount: float) -> Account:
        for index, item in enumerate(account_table[client_id]):
            if item.account_id == account_number:
                account_table[client_id][index].balance += amount
        return self.get_account_by_account_number(client_id, account_number)

    def withdraw(self, client_id: int, account_number: int, amount: float) -> Account:
        for index, item in enumerate(account_table[client_id]):
            if item.account_id == account_number:
                account_table[client_id][index].balance -= amount
        return self.get_account_by_account_number(client_id, account_number)

    def transfer(self, client_id: int, transfer_from: int, transfer_to: int, amount: float) -> List[Account]:
        both_accounts = list()

        for index, item in enumerate(account_table[client_id]):
            if item.account_id == transfer_from:
                account_table[client_id][index].balance -= amount
                both_accounts.append(item)
            elif item.account_id == transfer_to:
                account_table[client_id][index].balance += amount
                both_accounts.append(item)
        return both_accounts
