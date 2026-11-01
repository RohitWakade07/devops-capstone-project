# Accounts Service

![Build Status](https://github.com/RohitWakade07/accounts-service/actions/workflows/ci-build.yaml/badge.svg)

Flask REST API for managing customer accounts (create, read, list, update, delete), with Talisman security headers and CORS.

## Run
```bash
pip install -r requirements.txt
flask --app wsgi run        # http://localhost:5000
nosetests                   # run tests
docker build -t accounts .  # container on port 8080
```
