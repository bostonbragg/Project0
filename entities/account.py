class Account:
    def __init__(self, account_id: int, client_id: int, name: str, balance: float):
        self.account_id = account_id
        self.client_id = client_id
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"id: {self.account_id}, name: {self.name}, balance: {self.balance}"

    def as_json_dict(self):
        return {
            "accountID": self.account_id,
            "clientID": self.client_id,
            "name": self.name,
            "balance": self.balance
        }
