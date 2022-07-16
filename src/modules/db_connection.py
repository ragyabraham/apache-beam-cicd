import pymysql
import logging
from pymysql.constants import CLIENT
import traceback
import os
from dotenv import load_dotenv
from pathlib import Path
from modules.cloud_secrets import access_secret

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
LOCAL = os.getenv('LOCAL')

if LOCAL != 'True':
    PASSWORD = access_secret(
        'monitoring-db-rapmonusr',
        'latest')
    HOST = access_secret(
        'db_host',
        'latest')
    DB = access_secret(
        'db_name',
        'latest')
    USER = access_secret(
        'db_user',
        'latest')


def sql_get(query, params):
    print("==Running SQL Module==")
    if LOCAL == 'True':
        connection = pymysql.connect(
            # host='host.docker.internal',
            host='127.0.0.1',
            user='rapmonusr',
            password='password',
            database='RAPTOR_MONITORING_APP',
            port=3306,
            client_flag=CLIENT.MULTI_STATEMENTS)
    else:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB,
            port=3306,
            client_flag=CLIENT.MULTI_STATEMENTS)
    logging.info(f"SQL Connection: {connection}")
    logging.info(f"SQL Query: {query}")
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (params))
            results = cursor.fetchall()
            return results
    except ConnectionError as con_err:
        for i in range(0, len(con_err.args)):
            logging.error(con_err.args[i])
            traceback.print_tb(con_err.__traceback__)
    except Exception as err:
        for i in range(0, len(err.args)):
            logging.error(err.args[i])
            traceback.print_tb(err.__traceback__)
    finally:
        connection.close()
