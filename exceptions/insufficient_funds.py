class InsufficientFundsError(Exception):

    description: str = 'Occurs when an account does not have sufficient funds for a transaction'

    def __init__(self,message: str):
        self.message = message

