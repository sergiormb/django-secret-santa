[![Build Status](https://travis-ci.org/sergiormb/django-secret-santa.svg?branch=master)](https://travis-ci.org/sergiormb/django-secret-santa)
[![Coverage Status](https://coveralls.io/repos/github/sergiormb/django-secret-santa/badge.svg?branch=master)](https://coveralls.io/github/sergiormb/django-secret-santa?branch=master)

# Django Secret Santa #

A project made in Django 1.10 for the exchange of gifts at Christmas

## Features ##

- Compatible with python 2.7 and 3.4
- [Django debug toolbar](http://django-debug-toolbar.readthedocs.org/) enabled for superusers.

## Quickstart ##

First create and activate your virtualenv, you can use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/). Then install Django 1.10 in your virtualenv:

cd to your project and install the dependences

    pip install -r requirements.txt
 
    python manage.py migrate

    python manage.py collectstatic --link

Once everything it's setup you can run the development server: [http://localhost:8000/](http://localhost:8000/)

    python manage.py runserver


