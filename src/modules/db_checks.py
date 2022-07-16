from dotenv import load_dotenv
from pathlib import Path
from modules.sql_connection import sql_get
from modules.cloud_secrets import access_secret
import logging
import os
import redis

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

LOCAL = os.getenv('LOCAL')

if LOCAL == 'True':
    REDISHOST = "localhost"
    REDISPORT = 6379
else:
    REDISHOST = access_secret(
        'redis_host',
        'latest')
    REDISPORT = access_secret(
        'redis_port',
        'latest')
redis_client = redis.Redis(
    host=REDISHOST,
    port=REDISPORT)


class db_checks():

    def __init__(self, user, container):
        self.ext_user_id = user
        self.ext_container_id = container
        self.containers = None
        self.api_limit = None

    def execute_check(self):
        exists_redis = db_checks.check_redis(self)
        if exists_redis:
            logging.info("==Found in Redis==")
            return True
        else:
            logging.warning("==Not in Redis==")
            logging.warning("==Looking in SQL==")
            exists_db = db_checks.check_db(self)
            if exists_db:
                logging.warning("==Found in SQL==")
                try:
                    db_checks.update_redis(self)
                    logging.warning("==Updated Redis==")
                except Exception as err:
                    logging.error("==Something Went Wrong==")
                    logging.error(err.args[0])
            else:
                logging.info("==User Does Not Exists==")
                return True

    def check_db(self):
        sql_get_user = """
        SELECT
            U.USER_ID,
            UC.CONTAINER_ID,
            UL.OVER_LIMIT
        FROM USERS U
            LEFT JOIN USER_CONTAINERS UC
                ON UC.USER_ID = U.USER_ID
            LEFT JOIN USER_LIMITS UL
                ON UL.USER_ID = UC.USER_ID
        WHERE
            U.USER_EXTERNAL_ID = %s
            AND U.IS_ACTIVE = 1
            AND UC.IS_ACTIVE = 1;"""
        user_object = sql_get(
            sql_get_user,
            [self.ext_user_id])
        if user_object is not None:
            logging.info(f"User Obj: '{user_object}'")
            if len(user_object) > 0:
                self.api_limit = user_object[0][2]
                if self.api_limit == 0 or self.api_limit is None:
                    self.containers = [x[1] for x in user_object]
                    if self.ext_container_id in self.containers:
                        return True
                    else:
                        logging.warning("==Can't Find Container==")
                        db_checks.update_redis(self)
                        return True
                else:
                    logging.warning("==User Over Limit==")
                    db_checks.update_redis(
                        self,
                        overLimit=True)
                    return True
            else:
                logging.warning("==Length of User Object is 0==")
                return True
        else:
            logging.warning("==User Object is None==")
            return True

    def check_redis(self):
        redis_user = redis_client.hlen(
            self.ext_user_id)
        if redis_user:
            redis_limit = redis_client.hexists(
                self.ext_user_id,
                "overLimit")
            if redis_limit:
                redis_limit = redis_client.hget(
                    self.ext_user_id,
                    "overLimit").decode("utf-8")
                if redis_limit == "0":
                    redis_containers = redis_client.hexists(
                        self.ext_user_id,
                        "containerIds")
                    if redis_containers:
                        redis_containers = redis_client.hget(
                            self.ext_user_id,
                            "containerIds").decode("utf-8").split("|")
                        if self.ext_container_id in redis_containers:
                            return True
                        else:
                            return True
                    else:
                        return True
                else:
                    return True
            return True
        return True

    def update_redis(self, overLimit=True):
        try:
            if overLimit:
                redis_client.hset(
                    self.ext_user_id,
                    "overLimit", self.api_limit)
                return True
            else:
                redis_client.hset(
                    self.ext_user_id,
                    "containerIds", ('|').join(self.containers))
                redis_client.hset(
                    self.ext_user_id,
                    "overLimit", self.api_limit)
                return True
        except Exception as err:
            logging.error(err.args[0])
