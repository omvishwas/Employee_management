from os import environ

DB_PWD=environ.get('POSTGRES_PASSWORD','97cfd0c9')
DB_PORT=environ.get('POSTGRES_PORT','5432')
DB_USERNAME=environ.get("POSTGRES_USER",'postgres')
DB_HOST=environ.get('POSTGRES_HOST','localhost')
DB_NAME=environ.get('POSTGRES_DB','postgres')