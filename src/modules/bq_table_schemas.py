from google.cloud import bigquery

adobe_data_schema = [
    bigquery.SchemaField("event_id", "STRING"),
    bigquery.SchemaField("event_timestamp", "TIMESTAMP"),
    bigquery.SchemaField("company_org_id", "STRING"),
    bigquery.SchemaField("property_name", "STRING"),
    bigquery.SchemaField("property_id", "STRING"),
    bigquery.SchemaField("url", "STRING"),
    bigquery.SchemaField("login_state", "BOOLEAN"),
    bigquery.SchemaField("session_id", "STRING"),
    bigquery.SchemaField("segment_id", "STRING"),
    bigquery.SchemaField("user_id", "STRING"),
    bigquery.SchemaField("rule_name", "STRING"),
    bigquery.SchemaField("rule_id", "STRING"),
    bigquery.SchemaField("status", "STRING"),
    bigquery.SchemaField("ip_address", "STRING"),
    bigquery.SchemaField("latitude", "DECIMAL"),
    bigquery.SchemaField("longitude", "DECIMAL"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("region", "STRING"),
    bigquery.SchemaField("city", "STRING"),
    bigquery.SchemaField("timezone", "STRING"),
    bigquery.SchemaField("eu_member", "BOOLEAN"),
    bigquery.SchemaField("browser", "STRING"),
    bigquery.SchemaField("browser_version", "STRING"),
    bigquery.SchemaField("os", "STRING"),
    bigquery.SchemaField("os_version", "STRING"),
    bigquery.SchemaField("device", "STRING"),
    bigquery.SchemaField("action_modulepath", "STRING"),
    bigquery.SchemaField("action_modulepath_sum", "STRING"),
    bigquery.SchemaField("condition_modulepath", "STRING"),
    bigquery.SchemaField("condition_modulepath_sum", "STRING"),
    bigquery.SchemaField("event_modulepath", "STRING"),
    bigquery.SchemaField("event_modulepath_sum", "STRING"),
    bigquery.SchemaField("event_rule_order", "STRING"),
    bigquery.SchemaField("build_date", "TIMESTAMP"),
    bigquery.SchemaField("build_environment", "STRING"),
    bigquery.SchemaField("build_minified", "BOOLEAN"),
    bigquery.SchemaField("turbine_build_date", "TIMESTAMP"),
    bigquery.SchemaField("turbine_version", "STRING")
]