# Hello_books_api

![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/Xerrex/hello_books_api.svg?branch=master)](https://travis-ci.org/Xerrex/hello_books_api)

## Introduction
This is a Flask API for Hello-Books application. Hello-Books
helps manage a library and its processes like stocking, tracking and renting books.

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

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3.6 venv
        $ pip install autoenv

* #### Environment Variables
    Create a .env file and add the following:
    ```
    source venv/bin/activate
    ```