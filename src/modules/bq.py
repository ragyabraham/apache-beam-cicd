from google.cloud import bigquery
import os
from dotenv import load_dotenv
import google.auth
from pathlib import Path
import logging
import modules.bq_table_schemas as bq_table_schemas

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

LOCAL = os.getenv('LOCAL')

table_schemas = {
    'adobe_data': 'adobe_data_schema'
}


class bq():

    def __init__(self, table_name, ext_user_id, json_file):
        if LOCAL == 'True':
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./src/keys/k8s_owner_key.json"
        credentials, your_project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.ext_user_id = ext_user_id,
        self.bq_client = bigquery.Client(credentials=credentials)
        self.dataset = self.bq_client.dataset(self.ext_user_id[0])
        self.table_name = table_name
        self.table_id = "{}.{}.{}".format(
            self.bq_client.project,
            ext_user_id,
            self.table_name)
        if self.table_name == 'adobe_data':
            json_file[0].pop("settings", None)
            self.data = json_file
        else:
            self.data = json_file
        self.schema = getattr(
            bq_table_schemas,
            table_schemas[self.table_name])

    def check_column_exists(self):
        table_columns = list()
        json_keys = list()
        for column in self.table.schema:
            table_columns.append(column.name.lower())
        if isinstance(self.data, dict):
            for key in self.data.keys():
                json_keys.append(key)
        elif isinstance(self.data, list):
            for key in self.data[0].keys():
                json_keys.append(key.lower())
        columns_to_add = set(json_keys).difference(set(table_columns))
        if len(columns_to_add) > 0:
            logging.info(
                f"Found {len(columns_to_add)} Columns to add to schema")
            return False, columns_to_add
        else:
            return True, columns_to_add

    def add_column_to_schema(self, columns_to_add):
        original_schema = self.table.schema
        new_schema = original_schema[:]  # Creates a copy of the schema.
        for column_name in columns_to_add:
            new_schema.append(bigquery.SchemaField(
                column_name, "STRING"))
        self.table.schema = new_schema
        self.table = self.bq_client.update_table(
            self.table, ["schema"])
        # Make an API request.
        if len(self.table.schema) == len(original_schema) + len(columns_to_add) == len(new_schema):
            logging.info(
                f"{len(columns_to_add)} columns has been added.")
            return True
        else:
            logging.info("The column addition failed")
            return False

    def does_table_exist(self):
        try:
            self.table = self.bq_client.get_table(self.table_id)
            return True
        except Exception as err:
            logging.info("Table does not exists {}".format(err))
            return False

    def load_json_to_bq(self):
        try:
            if bq.does_table_exist(self):
                pass
                logging.info(f"==Table:'{self.table_id}' exists==")
            else:
                try:
                    logging.info(
                        "Table '{}' does not exists...Creating table".format(self.table_name))
                    table_ref = self.dataset.table(self.table_name)
                    table = bigquery.Table(table_ref, self.schema)
                    self.table = self.bq_client.create_table(table)
                    logging.info(
                        "Table '{}' Created Successfully".format(self.table_name))
                except Exception as err:
                    logging.error(err.args[0])
                    raise Exception("==Table Creation Failed for Table: '{}'==".format(
                        self.table_name))
            column_exists, columns_to_add = bq.check_column_exists(
                self)
            if column_exists is not True:
                bq.add_column_to_schema(self, columns_to_add)
            try:
                bq_response = self.bq_client.insert_rows_json(
                    self.table_id,
                    self.data,
                    row_ids=[None] * len(self.data))
                if len(bq_response) > 0:
                    if 'errors' in bq_response[0].keys():
                        if len(bq_response[0].get('errors')) > 0:
                            for i in range(len(bq_response[0].get('errors'))):
                                logging.error(
                                    f"Error: '{bq_response[0].get('errors')[i].get('message')}' was found at location: '{bq_response[0].get('errors')[i].get('location')}'")
                                raise Exception(
                                    f"Error: '{bq_response[0].get('errors')[i].get('message')}' was found at location: '{bq_response[0].get('errors')[i].get('location')}'")
                else:
                    logging.info(
                        f"==Successfully Loaded Data to {self.table_name} Table==")
            except Exception as e:
                logging.error(e.args[0])
                raise Exception('==BQ Insert Failed==')
        except Exception as err:
            logging.error(err.args[0])


if __name__ == '__main__':
    print("==Running Individual Module==")
