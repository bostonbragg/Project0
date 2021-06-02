from abc import abstractmethod, ABC
from typing import List
from entities.account import Account


class AccountDAO(ABC):
    # CREATE
    @abstractmethod
    def create_account(self, client_id: int) -> Account:
        pass

    # READ
    @abstractmethod
    def get_accounts_by_client_id(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def get_accounts_between(self, client_id: int, lower_bound: int, upper_bound: int) -> List[Account]:
        pass

    @abstractmethod
    def get_account_by_account_number(self, client_id: int, account_number: int) -> Account:
        pass

    # UPDATE
    @abstractmethod
    def update_account(self, client_id: int, account_number: int, account: Account) -> Account:
        pass

    @abstractmethod
    def deposit(self, client_id: int, account_number: int, amount: float) -> Account:
        pass

    @abstractmethod
    def withdraw(self, client_id: int, account_number: int, amount: float) -> Account:
        pass

    @abstractmethod
    def transfer(self, client_id: int, transfer_from: int, transfer_to: int, amount: float) -> List[Account]:
        pass

    # DELETE
    @abstractmethod
    def delete_account(self, client_id: int, account_number: int):
        pass
