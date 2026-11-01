"""REST routes for accounts."""
from flask import jsonify, request, abort
from service import app
from service.models import Account, DataValidationError

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404


@app.route("/")
def index():
    """Root URL"""
    return jsonify(name="Account REST API Service", version="1.0", paths="/accounts"), HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Create an Account"""
    account = Account()
    try:
        account.from_dict(request.get_json(silent=True))
    except DataValidationError as error:
        abort(HTTP_400_BAD_REQUEST, str(error))
    account.create()
    location = f"/accounts/{account.id}"
    return jsonify(account.to_dict()), HTTP_201_CREATED, {"Location": location}


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    return jsonify([a.to_dict() for a in Account.all()]), HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    """Read an Account"""
    account = Account.find(account_id)
    if not account:
        abort(HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return jsonify(account.to_dict()), HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """Update an Account"""
    account = Account.find(account_id)
    if not account:
        abort(HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    try:
        account.from_dict(request.get_json(silent=True))
    except DataValidationError as error:
        abort(HTTP_400_BAD_REQUEST, str(error))
    account.update()
    return jsonify(account.to_dict()), HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """Delete an Account"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", HTTP_204_NO_CONTENT


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(error):
    """Return errors as JSON"""
    return jsonify(status=error.code, error=error.name, message=error.description), error.code
