from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta

from closed_loop_controller import convert_to_seconds, limit_or_constant


def message():  # Just a quick message for the program to recognise it has loaded in
    print(f"Input plugin loaded: SQL")


def return_to_main(**kwargs):  # return to main function

    # just collects the kwargs (wanted to make code more readable)
    interval_seconds = convert_to_seconds(kwargs['interval'])
    database_connection = kwargs['database_connection']
    table = kwargs['table']
    changing_variable = kwargs['changing_variable']
    limorconst, constant_variable = limit_or_constant(kwargs)

    # this takes away the interval so the data is from the right time range
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    time_minus_interval = (datetime.now() - timedelta(seconds=interval_seconds)).strftime("%Y-%m-%d %H:%M:%S.%f")

    if limorconst:
        sql = f"""SELECT
               avg({changing_variable}) as {changing_variable},
               avg({constant_variable}) as {constant_variable}
        FROM {table}
        WHERE
              time BETWEEN '{time_minus_interval}' AND '{time_now}'"""
    elif limorconst is False:
        sql = f"""SELECT
               avg({changing_variable}) as {changing_variable}
        FROM {table}
        WHERE
              time BETWEEN '{time_minus_interval}' AND '{time_now}'"""

    with create_engine(database_connection).connect() as con:
        # safety connects to the database and runs the sql script and then closes the connection
        tmp = pd.read_sql(sql=sql,
                          con=con,
                          )

    return tmp.iloc[0].to_dict()  # return as a dictionary
