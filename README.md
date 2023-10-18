# inventory-management-system-backend

## Install required packages
- `pip install django`
- `pip install djangorestframework`

## Virtual environment
It is recommended to use a python virtual environment:
- Install package `virtualenv`: `pip install virtualenv`
- Create virtual environment using; `python -m venv env`
- Activate (windows) using: `.\env\Scripts\activate`
- Deactivate (windows) using: `.\env\Scripts\deactivate`

## TODO

Tener dos grupos: admin y warehouse_keeper

(OK) Que el que no se encuentre autenticado no pueda hacer nada

(??) Que los usuario que pertenezcan al grupo admin puedan leer y modificar todo (si se crea superuser se puede hacer esto pero no hay grupo admin creado)

Que los warehouse_keeper puedan:
ver y agregar pero no modificar ni borrar marcas, categorias, productos, y moviemientos y no tocar usuarios

(??) Que se pueda registrar usuarios (por ahora solo se puede crear usuarios admin con python manage.py createsuperuser, revisar este tutorial para ver lo del registro: https://www.youtube.com/watch?v=AfYfvjP1hK8&t=1579s)

(OK) Que se pueda hacer login (usa simpleJWT)

Que retorne lo que se necesita para las graficas unicamente al admin (habría que pensar como darle permiso de hacer queries (se exponen endpoinst para esto: https://docs.djangoproject.com/en/4.2/topics/db/queries/)

