"""Account model."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DataValidationError(Exception):
    """Raised when data is missing or invalid."""


class Account(db.Model):
    """Class that represents an Account."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(256))

    def __repr__(self):
        return f"<Account {self.name} id=[{self.id}]>"

    def to_dict(self):
        """Serialize to a dict"""
        return {"id": self.id, "name": self.name, "email": self.email, "address": self.address}

    def from_dict(self, data):
        """Deserialize from a dict"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
        except (KeyError, TypeError) as error:
            raise DataValidationError("Invalid account: missing " + str(error)) from error
        return self

    def create(self):
        """Save a new account"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Save changes"""
        db.session.commit()

    def delete(self):
        """Delete the account"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """All accounts"""
        return cls.query.all()

    @classmethod
    def find(cls, account_id):
        """Find by id"""
        return db.session.get(cls, account_id)
