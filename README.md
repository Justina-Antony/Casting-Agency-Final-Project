# Casting Agency Service

## Overview

The Casting Agency project is a web application designed to manage the information of actors and movies within a casting agency. It provides functionalities for adding, updating, deleting, and retrieving information about actors and movies. The project aims to streamline the management of casting-related data for efficient decision-making and organization within the agency.

## Getting Started

1. The Casting Agency app is deployed to Render.
Base URL:  https://casting-agency-final-project-1.onrender.com/
2. Authentication: This application requires auth0 token for accessing the APIs.

### Installing Dependencies

#### Python 3.12

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies for running the application:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

## Models:

- **Movie** with attributes title and release date
- **Actor** with attributes name, age and gender

Postgres database connection details and model classes in models.py

## Endpoints:

```python
GET /actors 
GET /movies
----------------------
GET /movies/<int:id>
GET /actors/<int:id>
-----------------------
DELETE /actors/<int:id> 
DELETE /movies/<int:id>
-----------------------
POST /actors 
POST /movies
-----------------------
PATCH /actors/<int:id> 
PATCH /movies/<int:id>

These APIs are created in api.py file
```

### Setup Auth0

1. Create new Auth0 Domain with the Algorithm
2. Create API audience
3. Create new API permissions:
   - `get:movies`
   - `get:actors`
   - `post:movies`
   - `post:actors`
   - `patch:movies`
   - `patch:actors`
   - `delete:movies`
   - `delete:actors`
4. Create new roles for:
   - Casting Assistant
     - can `get:movies`
     - can `get:actors`
   - Casting Director
     - can `get:movies`
     - can `get:actors`
     - can `post:actors`
     - can `delete:actors`
     - can `patch:movies`
     - can `patch:actors`
   - Executive Producer
     - can perform all actions
7. Test your endpoints from postman using the generated Bearer Token

### Running the server

Ensure working using your created virtual environment.

Open a new terminal session, execute:

```bash
export FLASK_APP=api.py;
```

To enable debug mode on:

```bash
export FLASK_DEBUG=1
```

To run the server, execute:

```bash
flask run --reload
```

## Deploy to Render

 - Connect your Postgres with the Render
 - Create web service for Casting Agency Service by passing Database URL.

 Below curl to execute the APIs via CURL or Postman.
For example:

```bash
$ curl -X GET 'https://casting-agency-final-project-1.onrender.com/movies' \ --header 'Authorization: Bearer <access-token>'
$ curl -X GET 'https://casting-agency-final-project-1.onrender.com/movies/1' \ --header 'Authorization: Bearer <access-token>'
$ curl -X POST 'https://casting-agency-final-project-1.onrender.com/movies' \ --header 'Authorization: Bearer <access-token>'
$ curl -X PATCH --request PATCH 'https://casting-agency-final-project-1.onrender.com/movies/1' \ --header 'Authorization: Bearer <access-token>'
$ curl -X DELETE --request DELETE 'https://casting-agency-final-project-1.onrender.com/movies/1' \
--header 'Authorization: Bearer <access-token>'

$ curl -X GET 'https://casting-agency-final-project-1.onrender.com/actors' \ --header 'Authorization: Bearer <access-token>'
$ curl -X GET 'https://casting-agency-final-project-1.onrender.com/actors/1' \ --header 'Authorization: Bearer <access-token>' 
$ curl -X POST 'https://casting-agency-final-project-1.onrender.com/actors' \ --header 'Authorization: Bearer <access-token>'
$ curl -X PATCH --request PATCH 'https://casting-agency-final-project-1.onrender.com/actors/1' \ --header 'Authorization: Bearer <access-token>'
$ curl -X DELETE --request DELETE 'https://casting-agency-final-project-1.onrender.com/actors/1' \
--header 'Authorization: Bearer <access-token>'
```

## Testing:

Run our entire test case by running the following command at command line

```python
$ createdb castagency_test
$ psql -U postgres postres
$ python test_app.py
```