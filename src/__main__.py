from pathlib import Path
from dotenv import load_dotenv
import os
import logging
import apache_beam as beam
import json
from traceback import format_exc
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import google.auth

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# Load ENV variables
REGION = os.getenv('REGION')
BUCKET = os.getenv('BUCKET')
IMAGE = os.getenv('IMAGE')
LOCAL = os.getenv("LOCAL")
logging.info(f"Local enviornment is {LOCAL}")

if LOCAL == 'True':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./src/keys/k8s_owner_key.json"
    credentials, PROJECT_ID = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    runner = 'DirectRunner'
    TOPIC_ID = f"projects/{PROJECT_ID}/topics/beam-summit-testing"
    logging.info(f'Listening to Topic ID: {TOPIC_ID}')
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
else:
    credentials, PROJECT_ID = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    runner = 'DataflowRunner'
    TOPIC_ID = f"projects/{PROJECT_ID}/topics/beam-summit"
    logging.basicConfig(level=logging.ERROR)
    logging.getLogger().setLevel(logging.ERROR)


class GroupMessages(beam.PTransform):
    def expand(self, pcoll):
        return (
            pcoll
            | 'Pair with One' >> beam.Map(lambda x: (x, 1))
            | "Set Window" >> beam.WindowInto(beam.window.Sessions(1.0))
            | "Group By Key" >> beam.GroupByKey()
            | "Extract Message" >> beam.Map(lambda x: (x[0]))
            | "Convert to JSON" >> beam.Map(json.loads)
        )


class ParseAndJoin(beam.DoFn):
    def __init__(self):
        self.table_name = "adobe_data"

    def process(self, message):
        try:
            self.user_id = message.get('user_id')
            self.user_agent = message.get('user_agent')
            self.data = message
            self.data.pop('user_agent')
            from modules.parse_url import parse_and_join
            json_dict, self.event_id = parse_and_join(
                self.data,
                self.user_agent)
            res = {
                "data": json_dict,
                "userId": self.user_id,
                "tableName": self.table_name,
                "eventId": self.event_id
            }
            yield res
        except Exception as e:
            logging.error(e.args[0])
            logging.error(format_exc())


class WriteToBigQuery(beam.DoFn):
    def process(self, message):
        self.data = message.get('data')
        self.user_id = message.get('userId')
        self.table_name = message.get('tableName')
        try:
            from modules.bq import bq
            bq_load_data = bq(
                table_name=self.table_name,
                ext_user_id=self.user_id,
                json_file=self.data)
            bq_load_data.load_json_to_bq()
        except Exception as e:
            logging.error(e.args[0])
            logging.error(format_exc())


def run():
    # Creating pipeline options
    pipeline_options = PipelineOptions(
        runner=runner,
        project=PROJECT_ID,
        job_name=IMAGE,
        update=True,
        temp_location=f'{BUCKET}/temp',
        region=REGION,
        streaming=True,
        enable_streaming_engine=True,
        setup_file='./setup.py',
        save_main_session=True,
        prebuild_sdk_container_engine='cloud_build',
        service_account_email=f'dataflow-service-account@{PROJECT_ID}.iam.gserviceaccount.com'
    )
    pipeline_options.view_as(StandardOptions).streaming = True
    # Defining our pipeline and its steps
    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Decrypt Token
        data = (
            pipeline
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(TOPIC_ID)
            | "Group Messages" >> GroupMessages()
        )
        # Parse and Join data -> WriteToBigQuery
        _ = (
            data
            | "Parse JSON and Join" >> beam.ParDo(ParseAndJoin())
            | "Write Data to BQ" >> beam.ParDo(WriteToBigQuery())
        )


if __name__ == "__main__":
    logging.info("==Running Job==")
    run()
