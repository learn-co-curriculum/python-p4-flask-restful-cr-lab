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

In this lab, we'll be building an API for a plant store! In addition to our
usual Rails code, there is code for a React frontend application in the `client`
directory.

The code for the frontend application is done. Your job is to create the Rails
API so that the `fetch` requests on the frontend work successfully.

***

## Instructions

The React application is in the `client` directory. To set it up, from the root
directory, run:

```console
$ npm install --prefix client
```

Using `--prefix client` will run the npm command within the `client` directory.

To set up your backend, run:

```console
$ bundle install
```

To see how the React application and Rails API are interacting, you can run the
Rails application in one terminal by running:

```console
$ rails s
```

Then, [open another terminal][new terminal] and run React:

```console
$ npm start --prefix client
```

[new terminal]: https://code.visualstudio.com/docs/editor/integrated-terminal#_managing-terminals

Each application will run on its own port on `localhost`:

- React: [http://localhost:4000](http://localhost:4000)
- Rails: [http://localhost:3000](http://localhost:3000)

Take a look through the components in the `client/src/components/` folder to get
a feel for what our app does. Note that the `fetch` requests in the frontend (in
`NewPlantForm` and `PlantPage`) don't include the backend domain:

```js
fetch("/plants");
// instead of fetch("http://localhost:3000/plants")
```

This is because we are [proxying][create-react-app proxying] these requests to
our API.

***

## Deliverables

### Model

Create a `Plant` model that matches this specification:

| Column Name | Data Type |
| ----------- | --------- |
| name        | string    |
| image       | string    |
| price       | decimal   |

**If you use a Rails generator, don't forget to pass the `--no-test-framework`
argument!**

After creating the `Plant` model, you can run `rails db:migrate db:seed` to run
your migration and add some sample data to your database.

Check your progress by running `rails c` and verifying that the plants were
created successfully!

### Routes

Your API should have the following routes as well as the associated controller
actions that return the appropriate JSON data:

#### Index Route

```txt
GET /plants


Response Body
-------
[
  {
    "id": 1,
    "name": "Aloe",
    "image": "./images/aloe.jpg",
    "price": 11.50
  },
  {
    "id": 2,
    "name": "ZZ Plant",
    "image": "./images/zz-plant.jpg",
    "price": 25.98
  }
]
```

#### Show Route

```txt
GET /plants/:id


Response Body
------
{
  "id": 1,
  "name": "Aloe",
  "image": "./images/aloe.jpg",
  "price": 11.50
}
```

#### Create Route

In your controller's `create` action, use strong params when creating the new
`Plant` object.

```txt
POST /plants


Headers
-------
Content-Type: application/json


Request Body
------
{
  "name": "Aloe",
  "image": "./images/aloe.jpg",
  "price": 11.50
}


Response Body
-------
{
  "id": 1,
  "name": "Aloe",
  "image": "./images/aloe.jpg",
  "price": 11.50
}
```

Once all the tests are passing, start up the React app and explore the
functionality to see how the routes you created are being used.

## Resources

- [What RESTful Actually Means](https://codewords.recurse.com/issues/five/what-restful-actually-means)
- [Flask-RESTful][frest]
- [HTTP request methods - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

[frest]: https://flask-restful.readthedocs.io/en/latest/
