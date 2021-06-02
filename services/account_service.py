from abc import ABC, abstractmethod
from collections import Set

from entities.account import Account


class AccountService(ABC):
    @abstractmethod
    def create_account(self, client_id: int) -> Account:
        pass

    @abstractmethod
    def get_accounts_by_client_id(self, client_id: int) -> Set[Account]:
        pass

    @abstractmethod
    def get_accounts_between(self, client_id: int, lower_bound: int, upper_bound: int) -> Set[Account]:
        pass

    @abstractmethod
    def get_account_by_account_number(self, client_id: int, account_number: int) -> Account:
        pass

    @abstractmethod
    def update_account(self, client_id: int, account_number: int, account: Account) -> Account:
        pass

    @abstractmethod
    def deposit(self, client_id: int, account_number: int, amount: float):
        pass

    @abstractmethod
    def withdraw(self, client_id: int, account_number: int, amount: float):
        pass

    @abstractmethod
    def transfer(self, client_id: int, transfer_from: int, transfer_to: int, amount: float):
        pass

    @abstractmethod
    def delete_account(self, client_id: int, account_number: int):
        pass

    @abstractmethod
    def check_client_validity(self, client_id: int) -> bool:
        pass

    @abstractmethod
    def check_account_validity(self, client_id: int, account_number: int) -> bool:
        pass

    @abstractmethod
    def check_funds(self, client_id: int, account_number: int, amount: float) -> bool:
        pass
