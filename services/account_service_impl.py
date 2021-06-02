from typing import List

from daos.account_dao import AccountDAO
from daos.client_dao import ClientDAO
from entities.account import Account
from exceptions.client_not_found import ClientNotFoundError
from exceptions.insufficient_funds import InsufficientFundsError
from services.account_service import AccountService


class AccountServiceImpl(AccountService):
    def __init__(self, account_dao: AccountDAO, client_dao: ClientDAO):
        self.account_dao: AccountDAO = account_dao

        # only used for checking the validity of the client id given, used in check_client_validity()
        self.client_dao: ClientDAO = client_dao

    def create_account(self, client_id: int) -> Account:
        self.check_client_validity(client_id)
        return self.account_dao.create_account(client_id)

    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        self.check_client_validity(client_id)
        return self.account_dao.get_accounts_by_client_id(client_id)

    def get_accounts_between(self, client_id: int, lower_bound: int, upper_bound: int) -> List[Account]:
        self.check_client_validity(int(client_id))
        return self.account_dao.get_accounts_between(client_id, lower_bound, upper_bound)

    def get_account_by_account_number(self, client_id: int, account_number: int) -> Account:
        self.check_client_validity(client_id)
        self.check_account_validity(client_id, account_number)
        return self.account_dao.get_account_by_account_number(client_id, account_number)

    def update_account(self, client_id: int, account_number: int, account: Account) -> Account:
        self.check_client_validity(client_id)
        self.check_account_validity(client_id, account_number)
        return self.account_dao.update_account(client_id, account_number, account)

    def deposit(self, client_id: int, account_number: int, amount: float):
        self.check_client_validity(client_id)
        self.check_account_validity(client_id, account_number)
        return self.account_dao.deposit(client_id, account_number, amount)

    def withdraw(self, client_id: int, account_number: int, amount: float):
        self.check_client_validity(client_id)
        self.check_account_validity(client_id, account_number)
        self.check_funds(client_id, account_number, amount)
        return self.account_dao.withdraw(client_id, account_number, amount)

    def transfer(self, client_id: int, transfer_from: int, transfer_to: int, amount: float):
        self.check_client_validity(client_id)
        self.check_account_validity(client_id, transfer_from)
        self.check_account_validity(client_id, transfer_to)
        self.check_funds(client_id, transfer_from, amount)
        return self.account_dao.transfer(int(client_id), int(transfer_from), int(transfer_to), int(amount))

    def delete_account(self, client_id: int, account_number: int):
        self.check_client_validity(client_id)
        self.check_account_validity(client_id, account_number)
        return self.account_dao.delete_account(client_id, account_number)

    def check_client_validity(self, client_id: int) -> bool:
        try:
            self.client_dao.get_client_by_id(client_id)
        except (TypeError, KeyError, ValueError, AttributeError):
            raise ClientNotFoundError(f"The client with id of {client_id} does not exist.")
        return True

    def check_account_validity(self, client_id: int, account_number: int) -> bool:
        try:
            self.account_dao.get_account_by_account_number(client_id, account_number)
        except (TypeError, KeyError, ValueError, AttributeError):
            raise ClientNotFoundError(f"The account with number {account_number} for client with id of {client_id} "
                                      f"does not exist.")
        return True

    def check_funds(self, client_id: int, account_number: int, amount: float) -> bool:
        account = self.get_account_by_account_number(client_id, account_number)
        balance = account.balance
        if balance < amount:
            raise InsufficientFundsError(f"Insufficient Funds: The account with number {account_number} for "
                                         f"client with id of {client_id} "
                                         f"has an insufficient balance of ${balance}, which is less than the "
                                         f"necessary amount of ${amount}.")
        return True