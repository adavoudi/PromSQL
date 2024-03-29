"""Miscellaneous functions for retrieving data from a sql database"""

import re
from typing import Dict
import pandas as pd
import sqlalchemy
import datetime
from promsql.constants import DEFAULT_CONFIGS, CUSTOM_CONFIGS, VAL_COL, TIME_COL


def get_db_engine(db_url: str) -> sqlalchemy.engine.Engine:
    """Creates an sqlalchemy engine

    Args:
        db_url (str): the url which is passed to the create_engine function 
            of sqlalchemy.

    Returns:
        sqlalchemy.engine.Engine: The created engine
    """
    if not hasattr(get_db_engine, "clients"):
        get_db_engine.clients = dict()
    if db_url in get_db_engine.clients:
        return get_db_engine.clients[db_url]
    engine = sqlalchemy.create_engine(db_url, echo=False)
    get_db_engine.clients[db_url] = engine
    return engine


def get_metric_configs(params: Dict) -> Dict:
    metric_name = params["metric_name"]
    if not hasattr(get_metric_configs, "configs"):
        get_metric_configs.configs = dict()
    if metric_name in get_metric_configs.configs:
        return get_metric_configs.configs[metric_name]

    configs = dict()
    for custom_config in CUSTOM_CONFIGS:
        if isinstance(custom_config["check"], str):
            regex = re.compile(custom_config["check"])
            if regex.match(metric_name):
                configs = custom_config
                break
        elif callable(custom_config["check"]):
            if custom_config["check"](params):
                configs = custom_config
                break

    for k, v in DEFAULT_CONFIGS.items():
        if k not in configs:
            configs[k] = v

    for k, v in configs.items():
        if isinstance(v, str):
            configs[k] = v.format(**params)
        elif callable(v):
            configs[k] = v(params)

    configs["DB"] = get_db_engine(configs["DB"])
    get_metric_configs.configs[metric_name] = configs
    return configs


def fetch_metric_data(
    metric_name: str,
    labels=Dict,
    start_datetime: datetime.datetime = None,
    end_datetime: datetime.datetime = None,
    offset: int = 0,
):
    configs = get_metric_configs(
        {
            "metric_name": metric_name,
            "labels": labels,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        }
    )
    if end_datetime is None:
        end_datetime = datetime.datetime.now()
    if start_datetime is None:
        start_datetime = end_datetime - datetime.timedelta(
            seconds=configs["LOOK_BEHIND_DURATION"]
        )

    start_datetime = start_datetime - datetime.timedelta(seconds=offset)
    end_datetime = end_datetime - datetime.timedelta(seconds=offset)

    where_clauses = []
    where_clauses.append(
        "{TIMESTAMP_COLUMN} in('%sZ', '%sZ')"
        % (start_datetime.isoformat(), end_datetime.isoformat())
    )
    for label_name, label_option in labels.items():
        if label_option["op"] == "=":
            op = "="
        elif label_option["op"] == "!=":
            op = "<>"
        else:
            raise NotImplementedError(
                f"Operator {label_option['op']} is not implemented!"
            )
        value = (
            f"'{label_option['value']}'"
            if isinstance(label_option["value"], str)
            else label_option["value"]
        )
        where_clauses.append(f"{label_name}{op}{value}")
    where_clause = (
        "WHERE " + " AND ".join(where_clauses) if len(where_clauses) > 0 else ""
    )
    sql_query = (
        """
        SELECT *
        FROM '{TABLE_NAME}'
    """
        + where_clause
    ).format(**configs)
    df = pd.read_sql(
        sql_query, configs["DB"], parse_dates=[configs["TIMESTAMP_COLUMN"]]
    ).rename(
        columns={
            configs["VALUE_COLUMN"]: VAL_COL,
            configs["TIMESTAMP_COLUMN"]: TIME_COL,
        }
    )
    if configs["TAG_COLUMNS"] is not None:
        df = df[configs["TAG_COLUMNS"] + [VAL_COL, TIME_COL]]
    print(df.count())
    print(sql_query)
    return df
