"""Tests for the accounts REST API."""
import os
os.environ["DATABASE_URI"] = "sqlite:///:memory:"

from unittest import TestCase  # noqa: E402
from service import app  # noqa: E402
from service.models import db, Account  # noqa: E402

BASE = "/accounts"
HTTPS = {"base_url": "https://localhost"}
DATA = {"name": "John", "email": "j@x.com", "address": "NY"}


class TestAccountService(TestCase):
    """Account service tests"""

    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.client = app.test_client()

    def _create(self):
        resp = self.client.post(BASE, json=DATA, **HTTPS)
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()

    def test_index(self):
        resp = self.client.get("/", **HTTPS)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Account REST API Service")

    def test_create_account(self):
        resp = self.client.post(BASE, json=DATA, **HTTPS)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("/accounts/", resp.headers["Location"])
        self.assertEqual(resp.get_json()["name"], "John")

    def test_create_bad_data(self):
        self.assertEqual(self.client.post(BASE, json={"name": "x"}, **HTTPS).status_code, 400)
        self.assertEqual(self.client.post(BASE, data="nope", **HTTPS).status_code, 400)

    def test_list_accounts(self):
        self._create()
        self._create()
        resp = self.client.get(BASE, **HTTPS)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 2)

    def test_read_account(self):
        acct = self._create()
        resp = self.client.get(f"{BASE}/{acct['id']}", **HTTPS)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["email"], "j@x.com")

    def test_read_not_found(self):
        self.assertEqual(self.client.get(f"{BASE}/0", **HTTPS).status_code, 404)

    def test_update_account(self):
        acct = self._create()
        new = dict(DATA, name="John R")
        resp = self.client.put(f"{BASE}/{acct['id']}", json=new, **HTTPS)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "John R")

    def test_update_not_found_and_bad(self):
        self.assertEqual(self.client.put(f"{BASE}/0", json=DATA, **HTTPS).status_code, 404)
        acct = self._create()
        self.assertEqual(self.client.put(f"{BASE}/{acct['id']}", json={}, **HTTPS).status_code, 400)

    def test_delete_account(self):
        acct = self._create()
        self.assertEqual(self.client.delete(f"{BASE}/{acct['id']}", **HTTPS).status_code, 204)
        self.assertEqual(self.client.get(f"{BASE}/{acct['id']}", **HTTPS).status_code, 404)
        self.assertEqual(self.client.delete(f"{BASE}/{acct['id']}", **HTTPS).status_code, 204)

    def test_security_headers(self):
        headers = self.client.get("/", **HTTPS).headers
        self.assertEqual(headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("default-src", headers["Content-Security-Policy"])
        self.assertEqual(headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_cors_header(self):
        headers = self.client.get("/", **HTTPS).headers
        self.assertEqual(headers["Access-Control-Allow-Origin"], "*")

    def test_model_repr(self):
        self.assertIn("John", repr(Account(id=1, name="John")))
