
from flask import Flask, request, jsonify
from werkzeug.exceptions import abort

from daos.account_dao_local import AccountDAOLocal
from daos.account_dao_postgres import AccountDAOPostgres
from daos.client_dao_local import ClientDAOLocal
from daos.client_dao_postgres import ClientDAOPostgres
from entities.account import Account
from entities.client import Client
from exceptions.account_not_found import AccountNotFoundError
from exceptions.client_not_found import ClientNotFoundError
from exceptions.insufficient_funds import InsufficientFundsError
from services.account_service_impl import AccountServiceImpl
from services.client_service_impl import ClientServiceImpl

client_dao = ClientDAOPostgres()
account_dao = AccountDAOPostgres()
client_service = ClientServiceImpl(client_dao)
account_service = AccountServiceImpl(account_dao, client_dao)


def create_routes(app: Flask):
    @app.route("/clients", methods=["POST"])
    def create_new_client():
        client = client_service.create_client()
        client_id = client.client_id
        return jsonify(client.as_json_dict()), 201

    @app.route("/clients", methods=["GET"])
    def get_all_clients():
        clients = client_service.get_all_clients()
        dict_list = [client.as_json_dict() for client in clients]
        return jsonify(dict_list), 200

    @app.route("/clients/<client_id>", methods=["GET"])
    def get_client(client_id: int):
        try:
            client = client_service.get_client_by_id(client_id)
            return jsonify(client.as_json_dict()), 200
        except ClientNotFoundError as e:
            return e.message, 404

    @app.route("/clients/<client_id>", methods=["PUT"])
    def update_client(client_id: int):
        try:
            body = request.json
            client = Client(0, "")
            try:
                client = Client(int(body["clientID"]), body["clientName"])
            except KeyError:
                abort(400, 'Body must contain a client in JSON form.')
            updated = client_service.update_client(int(client_id), client)
            return jsonify(updated.as_json_dict()), 200
        except ClientNotFoundError as e:
            return e.message, 404

    @app.route("/clients/<client_id>", methods=["DELETE"])
    def delete_client(client_id: int):
        try:
            client_service.delete_client(int(client_id))
            return f"The client with id of {client_id} has been deleted successfully", 205
        except ClientNotFoundError as e:
            return e.message, 404

    @app.route("/clients/<client_id>/accounts", methods=["POST"])
    def create_account(client_id: int):
        try:
            account = account_service.create_account(int(client_id))
            return jsonify(account.as_json_dict()), 201
        except ClientNotFoundError as e:
            return e.message, 404

    @app.route("/clients/<client_id>/accounts", methods=["GET"])
    def get_accounts_by_client_id(client_id: int):
        try:
            upper_bound = request.args.get("amountLessThan", None)
            lower_bound = request.args.get("amountGreaterThan", None)

            if lower_bound is not None and upper_bound is not None:
                accounts = account_service.get_accounts_between(int(client_id), int(lower_bound), int(upper_bound))
            else:
                accounts = account_service.get_accounts_by_client_id(int(client_id))

            dict_list = [account.as_json_dict() for account in accounts]
            return jsonify(dict_list), 200
        except ClientNotFoundError as e:
            return e.message, 404

    @app.route("/clients/<client_id>/accounts/<account_number>", methods=["GET"])
    def get_account_by_account_number(client_id: int, account_number: int):
        try:
            account = account_service.get_account_by_account_number(int(client_id), int(account_number))
            return jsonify(account.as_json_dict()), 200
        except (ClientNotFoundError, AccountNotFoundError) as e:
            return e.message, 404

    @app.route("/clients/<client_id>/accounts/<account_number>", methods=["PUT"])
    def update_account(client_id: int, account_number: int):
        try:
            body = request.json
            account = Account(int(body["accountID"]), int(body["clientID"]), body["name"], int(body["balance"]))
            updated = account_service.update_account(int(client_id), int(account_number), account)
            return jsonify(updated.as_json_dict()), 200
        except (ClientNotFoundError, AccountNotFoundError) as e:
            return e.message, 404

    @app.route("/clients/<client_id>/accounts/<account_number>", methods=["DELETE"])
    def delete_account(client_id: int, account_number: int):
        try:
            account_service.delete_account(int(client_id), int(account_number))
            return f"Deleted account with number {account_number} for client {client_id}", 200
        except (ClientNotFoundError, AccountNotFoundError) as e:
            return e.message, 404

    @app.route("/clients/<client_id>/accounts/<account_number>", methods=["PATCH"])
    def withdraw_or_deposit(client_id: int, account_number: int):
        try:
            body = request.json

            try:
                amount = int(body["withdraw"])
                transaction_type = "withdraw"
            except KeyError:
                try:
                    amount = int(body["deposit"])
                    transaction_type = "deposit"
                except KeyError:
                    transaction_type = "none"

            if transaction_type == "deposit":
                updated = account_service.deposit(int(client_id), int(account_number), amount)
            elif transaction_type == "withdraw":
                updated = account_service.withdraw(int(client_id), int(account_number), amount)
            else:
                abort(400, 'Body must contain a deposit or withdraw amount in JSON form.')
                updated = ""

            return jsonify(updated.as_json_dict()), 200

        except (ClientNotFoundError, AccountNotFoundError, InsufficientFundsError) as e:
            if type(e) == ClientNotFoundError or type(e) == AccountNotFoundError:
                return e.message, 404
            elif type(e) == InsufficientFundsError:
                return e.message, 422

    @app.route("/clients/<client_id>/accounts/<transfer_from>/transfer/<transfer_to>", methods=["PATCH"])
    def transfer(client_id: int, transfer_from: int, transfer_to: int):
        try:
            body = request.json
            try:
                amount = int(body["amount"])
                both_accounts = account_service.transfer(int(client_id), int(transfer_from), int(transfer_to), amount)
                dict_list = [account.as_json_dict() for account in both_accounts]

                # return f"Successfully transferred ${amount} from account #{transfer_from} to account #{transfer_to} " \
                #        f"for client with id of {client_id}.\nCurrent balance of account #{transfer_from}: " \
                #        f"${both_accounts[0].balance}\nCurrent balance of account #{transfer_to}: " \
                #        f"${both_accounts[1].balance}.\n" + str(both_accounts[0].as_json_dict()) + "\n" \
                #        + str(both_accounts[1].as_json_dict()), 200
                return jsonify(dict_list), 200
            except KeyError:
                return "Body must contain a deposit or withdrawal amount in JSON form.", 400

        except (ClientNotFoundError, AccountNotFoundError, InsufficientFundsError, AttributeError) as e:
            if type(e) == ClientNotFoundError or type(e) == AccountNotFoundError:
                return e.message, 404
            elif type(e) == AttributeError:
                return 404
            elif type(e) == InsufficientFundsError:
                return e.message, 422
