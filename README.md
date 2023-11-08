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

## TODO

(  ) Que se pueda registrar usuarios (con contraseña) desde un endpoint: https://python.plainenglish.io/django-custom-user-model-and-auth-using-jwt-simple-boilerplate-6acd78bf7767)

(  ) Que se pueda modificar usuarios (con y sin contraseña) desde un endpoint: https://python.plainenglish.io/django-custom-user-model-and-auth-using-jwt-simple-boilerplate-6acd78bf7767). Asumimos que unicamente el warehouse_admin puede modificar los datos de los warehouse_users

(  ) Que retorne lo que se necesita para las graficas unicamente al admin (USAR los permisos de django_rest_framework y crear los permisos custom para esto) 

(  ) Arreglar permisos que no funcionan (keeper puede hacer get de users)

(  ) Definir unos endpoints que permitan obtener los datos para las graficas. Definir que deben retornar.

(  ) Crear desde codigo los grupo con los permisos que corresponden
### Notes

- In unix make a cron job to flush blacklisted tokens using `python manage.py flushexpiredtokens` https://osirusdjodji.medium.com/cron-job-in-django-with-django-crontab-c02bff68a96d
- Groups for warehouse-keeper and warehouse-admin are created manually using django admin UI.