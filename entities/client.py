class Client:
    def __init__(self, client_id: int, client_name: str):
        self.client_id = client_id
        self.client_name = client_name

    def __str__(self):
        return f"id: {self.client_id}, name: {self.client_name}"

    def as_json_dict(self):
        return {
            "clientID": self.client_id,
            "clientName": self.client_name
        }
