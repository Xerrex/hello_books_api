# Hello_books_api

![license](https://img.shields.io/github/license/mashape/apistatus.svg)

[![Build Status](https://travis-ci.org/Xerrex/hello_books_api.svg?branch=develop)](https://travis-ci.org/Xerrex/hello_books_api)

[![Coverage Status](https://coveralls.io/repos/github/Xerrex/hello_books_api/badge.svg?branch=develop)](https://coveralls.io/github/Xerrex/hello_books_api?branch=develop)

[![Test Coverage](https://api.codeclimate.com/v1/badges/f198d0ee5be9bc93d9d9/test_coverage)](https://codeclimate.com/github/Xerrex/hello_books_api/test_coverage)

## Introduction
This is a Flask API for Hello-Books application. Hello-Books
helps manage a library and its processes like stocking, tracking and renting books.

## EndPoints
* `GET:     /api/v1/books`  to get all books.
* `POST:    /api/v1/books` to add a book.
* `PUT:     /api/v1/books/<bookId>` to modify book details.
* `GET:     /api/v1/books/<bookId>` to view a book information.
* `DELETE:  /api/v1/books/<bookId>` to delete a book. 
* `POST:    /api/v1/auth/register` to register a new user.
* `POST:    /api/v1/auth/login` to login a user


## Technologies used
* **[Python3](https://www.python.org/downloads/)** - A programming language that lets you work more quickly (The universe loves speed!).
* **[Flask](flask.pocoo.org/)** - A microframework for Python based on Werkzeug, Jinja 2 and good intentions
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments

## Installation / Usage
* First ensure [python3.6](https://www.python.org) globally is installed in your computer

* Ensure virtualenv  is also installed globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone https://github.com/Xerrex/hello_books_api.git
    ```
    
* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd hello_books_api
        ```

    2. Create and activate virtual environment in python3:
        ```
        $ virtualenv -p python3.6 venv
        $ pip install autoenv

* #### Environment Variables
    Create a .env file and add the following:
    ```
    source venv/bin/activate
    export FLASK_APP="run.py"
    export FLASK_CONFIG='dev_env'
    export SECRET_KEY="add a very long random sentence or string "
    export FLASK_DEBUG=1
    
    ```
    Now navigating to this directory `Autoenv`automagically set the variables.Sensitive info 
    is hidden to outiside world too. 
    
    if not prompted by `Autoenv` run `source .env` to set variables.

* #### Install your requirements
    With virtual enviroment activated run:
    
    ```
    pip install -r requirements.txt
    ```    