from flask import current_app as app

from influxdb_client import InfluxDBClient
import pandas as pd

def sendQueryInflux(query):
    token = app.config['INFLUX_TOKEN']
    org = app.config['INFLUX_ORG']
    url = app.config['INFLUX_URL']

    client = InfluxDBClient(url=url, token=token, org=org, debug=False)
    df_result = client.query_api().query_data_frame(org=org, query=query)

    return df_result

def removeUselessColumns(df):
    df = df.drop(columns=['result', 'table', '_start', '_stop', '_measurement'])
    df = df.rename(columns={'_time': 'time', '_value': 'value', '_field': 'field'})

    return df