# Capstone Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is library to handle the database. Model file can be found in `models.py`. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Database Setup
With Postgres running, restore a database using the capstone.psql file provided. From the backend folder in terminal run:
```bash
psql capstone < capstone.psql
```

## Testing
To run the tests, run
```
dropdb capstone_test
createdb capsotne_test
psql capstone_test < capstone.psql
python3 test_app.py
```

## Running the server

From within the `./backend` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `delete:actors`
    - `delete:movies`
    - `get:actors`
    - `get:movies`
    - `patch:actors`
    - `patch:movies`
    - `post:actors`
    - `post:movies`
6. Create new roles for:
    - Casting Director
        - can perform all actions except `post:movies` and `delete:movies`
    - Executive Producer
        - can perform all actions

### The Server
Files are used to work the server.
1. `auth.py`
2. `app.py`
3. `models.py`