# import os
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# DATABASE_URI = 'mysql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
#     dbuser=os.environ['DBUSER'],
#     dbpass=os.environ['DBPASS'],
#     dbhost=os.environ['DBHOST'],
#     dbname=os.environ['DBNAME']
# )

# TIME_ZONE = 'UTC'

# STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
# STATIC_URL = 'static/'

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'flask-insecure-7ppocbnx@w71dcuinn*t^_mzal(t@o01v3fee27g%rg18fc5d@')

# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
# CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

# Configure Postgres database based on connection string of the libpq Keyword/Value form
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
# conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
# conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

DATABASE_URI = 'mysql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser='roberttracey',
    dbpass='i.r8D8UgyeltJ_wC',
    dbhost='f1db.mysql.database.azure.com',
    dbname='f1db'
)