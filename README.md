# Capstone-Backend API

The Capstone is a Casting Agency that is responsible for creating Movies and managing and assigning Actors to those Movies. There are two users Executive Producer and Casting Director within the company and are creating a system to simplify and streamline this process.

The Capstone code follows PEP8 style guidelines.

### Agency Tasks:
1) Display actors and movies list with details.
2) Allow Casting Director to add, delete Actors and edit Movie and Actor details.
3) Allow Executive Producer to create, delete Movies and all the permissoins that casting director has. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

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
createdb capstone_test
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

## Endpoints:

1. Get Actors

    GET '/actors'
    - Fetches all actors with detail: id, name, age, gender.
    - Request Arguments: None
    - Returns: An object actors with all the actors with id, name, age, gender.
    - curl https://capstone-agency-backend.herokuapp.com/actors
    - {
        "actors":[
                {
                    "age":55,
                    "gender":"Male",
                    "id":5,
                    "name":"Shahrukh Khan"
                },
        :
        :
        :
        ],
        "success":true
     }

2. Post Actor

    POST '/actors'
    - Insert actor into database with detail: name, age, gender.
    - Request Arguments: actor
    - Returns: An object actors with all the actors with id, name, age, gender.
    - curl -X POST  -H "Content-Type:application/json" -H "Authorization: Bearer $DIRECTOR_TOKEN" https://capstone-agency-backend.herokuapp.com/actors 
       -d '{"name":"Kristin Stewart","age":31,"gender":"Female"}'
    - {
        "actors":{
            "age":31,
            "gender":"Female",
            "id":17,
            "name":"Kristin Stewart"
        },
        "success":true
      }

3. Update Actor

    PATCH '/actors/<int:actor_id>'
    - Update actor's detail.
    - Request Arguments: actor_id
    - Returns: An object actor with id, name, age, gender.
    - curl -X PATCH https://capstone-agency-backend.herokuapp.com/actors/8 -H"Content-Type: application/json" -H "Authorization: Bearer $DIRECTOR_TOKEN"
       -d "{\"name\":\"Angie\",\"age\":22}"
    - {
        "actors":[
            {
                "age":22,
                "gender":"Female",
                "id":8,
                "name":"Angie"
            }
        ]
        ,"success":true
      }

4. Delete Actor

    DELETE '/actors/<int:actor_id>'
    - Delete actor from actor and movie_actor table.
    - Request Arguments: actor_id
    - Returns: An object delete with actor_id.
    - curl -X DELETE  -H "Content-Type:application/json" -H 
       "Authorization:Bearer $DIRECTOR_TOKEN" 
       https://capstone-agency-backend.herokuapp.com/actors/15
    - {
        "success": True,
        "delete": 15
      }

5. Get Movies

    GET '/movies'
    - Fetches all movies with detail: id, release_date, selected_actors, title.
    - Request Arguments: None
    - curl https://capstone-agency-backend.herokuapp.com/movies
    - {
        "movies":[
            {
                "id":1,
                "release_date":"Friday, 19 December 1997",
                "selected_actors":[
                    {
                        "id":8,
                        "name":"Angie"
                    },
                    {
                        "id":9,
                        "name":"George Clooney"
                    }
                ],
                "title":"Titanic"
            },
            :
            :
            :
        ],
        "success":true
      }

6. POST Movie

    POST '/movies'
    - Insert movie into database with detail: title, release_date.
    - Request Arguments: movie
    - Returns: An object actors with all the actors with id, title, release_date, selected_actor.
    - curl -X POST  -H "Content-Type:application/json" -H "Authorization:
             Bearer $PRODUCER_TOKEN" https://capstone-agency-backend.herokuapp.com/movies
             -d '{"title":"Captain Marvel", "release_date": "2019-03-04"}'
    - {
        "movies":[
            {
                "id":1,
                "release_date":"Monday, 4 March 2019",
                "selected_actors":[],
                "title":"Captain Marvel"
            },
        ],
        "success":true
      }

7. Assign actors to the movie

    PATCH '/movies/<int:movie_id>'
    - Assign actors to the Movie. Insert value to the movie and movie_actor table.
    - Request Arguments: movie_id
    - Returns: An object movie with detais: id, title, release_date, selected_actors.
    - curl -X PATCH https://capstone-agency-backend.herokuapp.com/movies/16 -H 
       "Content-Type: application/json" -H "Authorization: Bearer $DIRECTOR_TOKEN" 
       -d "{\"selected_actors\":[\"8\",\"9\"]}"
    - {
        "movie":[
            {
                "id":6,
                "release_date":"Wednesday, 05 May 2021",
                "selected_actors":[
                    {
                        "id":8,
                        "name":"Angie"
                    },
                    {
                        "id":9,
                        "name":"George Clooney"
                    }
                ],
                "title":"Godzilla"
            }
        ],
        "success":true
      }

8. Delete Movie

    DELETE '/movies/<int:movie_id>'
    - Delete movie from movie and movie_actor table.
    - Request Arguments: movie_id
    - Returns: An object delete with movie_id.
    - curl -X DELETE  -H "Content-Type:application/json" -H "Authorization:Bearer
       $PRODUCER_TOKEN" https://capstone-agency-backend.herokuapp.com/movies/18
    - {
        "success": True,
        "delete": 18
      }


## Error Handling

    Errors are returned as JSON objects in the following format:
    {
        "error": 404, 
        "message": "resource not found", 
        "success": false
    }

    The API will return six types of error when requests fail:

    1. 400: Bad Request
    2. 401: Authorization Error
    3. 404: Resource Not Found
    4. 405: Method Not Allowed
    5. 422: Unprocessable
    6. 500: Internal Server Error

### The Server

Files are used to work the server.
1. `auth.py`
2. `app.py`
3. `models.py`

### Deployment
**Capstone** application deployed in **_Heroku_**. This is the url for [**capstone**](https://capstone-agency-backend.herokuapp.com/movies).

### Author
Purvi Rawal

### Acknoledgemnts
Udacity team for making a greate nenodegree program for Full Stack Developer.