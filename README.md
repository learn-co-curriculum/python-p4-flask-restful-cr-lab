# REST Create and Retrieve Lab

## Learning Goals

- Build RESTful APIs that are easy for other developers to understand and use
  in their own applications.

***

## Key Vocab

- **Representational State Transfer (REST)**: a convention for developing
  applications that use HTTP in a consistent, human-readable, machine-readable
  way.
- **Application Programming Interface (API)**: a software application that
  allows two or more software applications to communicate with one another.
  Can be standalone or incorporated into a larger product.
- **HTTP Request Method**: assets of HTTP requests that tell the server which
  actions the client is attempting to perform on the located resource.
- **`GET`**: the most common HTTP request method. Signifies that the client is
  attempting to view the located resource.
- **`POST`**: the second most common HTTP request method. Signifies that the
  client is attempting to submit a form to create a new resource.
- **`PATCH`**: an HTTP request method that signifies that the client is attempting
  to update a resource with new information.
- **`PUT`**: an HTTP request method that signifies that the client is attempting
  to update a resource with new information contained in a complete record.
- **`DELETE`**: an HTTP request method that signifies that the client is
  attempting to delete a resource.

***

## Introduction

Flask as you've learned it is already a great tool for building RESTful APIs,
but it's important to always seek out the best tools for the job. There are
dozens of extensions designed exclusively for use with Flask, and one,
[Flask-RESTful][frest], makes it _very_ easy to build RESTful APIs.

***

## Flask-RESTful Example

Let's take a look at a bare-bones API built with Flask-RESTful:

```py
# example only

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Newsletter(Resource):
    def get(self):
        return {"newsletter": "it's a beautiful 108 out in Austin today"}

api.add_resource(Newsletter, '/newsletters')

if __name__ == '__main__':
    app.run()

```

We can run this app just like any other- with `python app.py` or `flask run`-
then navigate to the client in order to access `Newsletter`'s resources. Since
the data here is returned in such a simple format, we can access it most easily
from the command line with `curl`:

```console
$ curl http://127.0.0.1:5000
# => {"newsletter: "it's a beautiful 108 out in Austin today"}
```

So what's going on here?

### `Api` and `Resource`

Flask-RESTful's `Api` class is the constructor for your RESTful API as a whole.
It is initialized with a Flask application instance and populates with resources
later on. These resources all inherit from the `Resource` class, which includes
conditions for throwing exceptions and base methods for each HTTP method that
explicitly disallow them.

When `Resource` subclasses are added to the `Api` instance with
`add_resource()`, it uses the newly defined HTTP verb instance methods to
determine which routes to create at the provided URL.

`Api` and `Resource` aren't the only classes available to us through
Flask-RESTful, but they're more than enough to get us started.

### What's Missing?

Because the `Resource` class and `create_resource` methods handle tasks normally
carried out by the `@app.route()` decorator, we don't need to include the
decorator itself. Remember though: if you add any non-RESTful views to your app,
you still need `app.route()`!

***

## Getting Started

Enter your virtual environment with `pipenv install && pipenv shell`. Open
`newsletters/app.py` and enter the following code to create a RESTful index
page:

```py
#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):

    def get(self):
        
        response_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }
        
        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

api.add_resource(Index, '/')

```

Run `flask run` from the `newsletters/` directory and you should see the
following at [http://127.0.0.1:5000](http://127.0.0.1:5000):

```json
{
  "index": "Welcome to the Newsletter RESTful API"
}
```

Congratulations on creating your first RESTful API endpoint!

You'll notice that there are quite a few imports and lines of configuration that
relate to databases- we'll be working with one in this lesson, but the models
and migrations have already been created for you. When you're ready, run
`flask db upgrade` to create the database and `python seed.py` to seed it with
fake data.

***

## Retrieving Records with Flask-RESTful

Our index is a perfectly good example of a successful `GET` request, but it
doesn't truly allow other people's applications to interact with our newsletter
database. Let's set up another route, `/newsletters`, that returns all of the
records from the `newsletters` table. Open `newsletters/app.py` and enter the
following beneath your `Index` view:

```py
# newsletters/app.py

class Newsletters(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

api.add_resource(Newsletters, '/newsletters')

```

While the outside structure of views in Flask-RESTful is quite different from
vanilla Flask, the internal structure is virtually the same. We can write each
of our views- for create, retrieve, update, and delete- just as we did before.
The main difference here is that instead of each HTTP verb getting a code block
inside of a view function, they each get an instance method inside of a
`Resource` class.

Run `flask run` from the `newsletters/` directory and you should see something
similar to the following at [http://127.0.0.1:5000/newsletters](
http://127.0.0.1:5000/newsletters):

```json
[
  {
    "body": "Create southern girl news. Image interesting mean professor federal agree. Clearly before seat threat during role provide.",
    "edited_at": null,
    "id": 1,
    "published_at": "2022-09-21 18:35:17",
    "title": "Establish they."
  },
  {
    "body": "Really attack we ground production game. Late agency example local break start. Tell leader new above just before. Participant southern thousand win group dream reason.",
    "edited_at": null,
    "id": 2,
    "published_at": "2022-09-21 18:35:17",
    "title": "Plan wonder manage."
  },
  {
    "body": "Will suffer choice impact. Audience happen write feel represent. Woman discover million kitchen. Although make little affect.",
    "edited_at": null,
    "id": 3,
    "published_at": "2022-09-21 18:35:17",
    "title": "Meet cut stuff."
  },
  ...
]
```

***

## Creating Records with Flask-RESTful

Let's move onto creating records with `POST` requests. Reopen
`newsletters/app.py` and add the following to the bottom of the `Newsletter`
class:

```py
# newsletters/app.py

def post(self):
    
    new_record = Newsletter(
        title=request.form['title'],
        body=request.form['body'],
    )

    db.session.add(new_record)
    db.session.commit()

    response_dict = new_record.to_dict()

    response = make_response(
        jsonify(response_dict),
        201,
    )

    return response

```

> **NOTE: We do NOT need to run the `add_resource()` method twice, as the `GET`
> and `POST` routes are accessible through the same `Resource` and URL.**

There's nothing you haven't seen before here: we retrieve form data through the
request context, use it to create a new Newsletter record, commit that record to
the database, then return it to the client with a 201 status code to denote that
it was created successfully.

Try it out for yourself: open Postman and navigate to
[http://127.0.0.1:5000/newsletters](http://127.0.0.1:5000/newsletters). Change
the request method to `POST`, edit the `Body > form-data` with a title and body,
then hit submit. You should see a response similar to the following:

```json
{
    "body": "This is the body of the newsletter entitled \"Mr. Title\".",
    "edited_at": null,
    "id": 51,
    "published_at": "2022-09-21 19:16:31",
    "title": "Mr. Title"
}
```

***

## Building Another Resource and Retrieving a Single Record

We won't always want to read _every_ newsletter, so we should probably build
a route to get a single record back from the database. There are a couple
things to consider before we begin:

1. A `GET` route already exists under `newsletters/`.
2. Retrieving a single record means that we need some sort of **id**entifier.

This means that we need to build a new `Resource` for this endpoint, and that
it should include the `id` in the URL. Let's give it a shot!

```py
# newsletters/app.py

class NewsletterByID(Resource):

    def get(self, id):

        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

```

Only two differences between this and our original `GET` route:

1. We need to include `id` in our method's arguments and the resource URL.
2. We need to chain some commands together to get the record with the provided
   `id`.

Check out this lesson's finished product: open Postman and navigate to
[http://127.0.0.1:5000/newsletters/20](http://127.0.0.1:5000/newsletters/20).
Make sure that your request method is `GET`, then click submit. You should see
something similar to the following:

```json
{
    "body": "College tax head change. Claim exactly because choose. Church edge center across test stock.",
    "edited_at": null,
    "id": 20,
    "published_at": "2022-09-21 18:35:17",
    "title": "Court probably not."
}
```

***

## Conclusion

Flask-RESTful is a very simple tool that allows us to properly and effectively
use HTTP request methods in our applications. Like other extensions, it reduces
the amount of code you have to write to accomplish common tasks- and if you
don't need to accomplish those common tasks, you can just leave it out!

***

## Solution Code

```py
#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):

    def get(self):
        
        response_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }
        
        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(Index, '/')

class Newsletters(Resource):

    def get(self):
        
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):
        
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):

    def get(self, id):

        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(NewsletterByID, '/newsletters/<int:id>')


if __name__ == '__main__':
    app.run()

```

## Resources

- [What RESTful Actually Means](https://codewords.recurse.com/issues/five/what-restful-actually-means)
- [Flask-RESTful][frest]
- [HTTP request methods - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

[frest]: https://flask-restful.readthedocs.io/en/latest/
