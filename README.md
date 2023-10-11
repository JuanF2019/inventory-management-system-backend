# inventory-management-system-backend

## Virtual environment
It is recommended to use a python virtual environment:
- Install package `virtualenv`: `pip install virtualenv`
- Create virtual environment using; `python -m venv env`
- Activate (windows) using: `.\env\Scripts\activate`
- Deactivate (windows) using: `.\env\Scripts\deactivate`

## Install required packages
- `pip install django`
- `pip install djangorestframework`

## Make database migration
- This creates the tables defined on models.py:
  - `python manage.py makemigrations`
  - `python manage.py migrate`

## Running the API on development mode
- Run `python manage.py runserver`

