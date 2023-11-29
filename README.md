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
- `pip install djangorestframework-simplejwt`

## Make database migration
- This creates the tables defined on models.py:
  - `python manage.py makemigrations`
  - `python manage.py migrate`

## Running the API on development mode
- Run `python manage.py runserver`

## Sample request
- On folder `sample_requests/` there is a file that can be imported to postman. It contains several sample request used during development.

### Notes

- In unix make a cron job to flush blacklisted tokens using `python manage.py flushexpiredtokens` https://osirusdjodji.medium.com/cron-job-in-django-with-django-crontab-c02bff68a96d
- Groups for warehouse-keeper and warehouse-admin are created manually using django admin UI.
- Contact me at `juan.martinez27@u.icesi.edu.co` if you have any trouble
