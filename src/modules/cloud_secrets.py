from traceback import format_exc
from google.cloud import secretmanager
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

PROJECT_ID = 'tag-monitoring-dev'
LOCAL = os.getenv("LOCAL")

if LOCAL == 'True':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./src/keys/k8s_owner_key.json"


def access_secret(secret_id, version_id):
    try:
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(
            request={
                "name": name
            }
        )
        payload = response.payload.data.decode('UTF-8')
        return payload
    except Exception as e:
        logging.error(e.args[0])
        logging.error(format_exc())
        return None
