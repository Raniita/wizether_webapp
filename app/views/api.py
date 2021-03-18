from flask import Blueprint, render_template, request, redirect, jsonify, url_for, g, send_file, current_app, flash
from flask import current_app as app
from flask_login import login_required, current_user
from rq import push_connection, pop_connection, Queue
import redis

from influxdb_client import InfluxDBClient
from datetime import datetime
from pathlib import Path
import pandas as pd
import os

from app import tasks
from app.forms import QueryAPI_DateRange_Field, QueryAPI_DateRange_All

api_bp = Blueprint('api', __name__, url_prefix='/api')
    

#
# Open API
#

@api_bp.route('/query_date_range', methods=['POST'])
@login_required
def query_date_range():

    token = app.config['INFLUX_TOKEN']
    org = app.config['INFLUX_ORG']
    bucket = app.config['INFLUX_BUCKET']
    url = app.config['INFLUX_URL']

    form = QueryAPI_DateRange_Field(request.form)
    if form.validate_on_submit():
        start = form.start_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        stop = form.stop_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        field = form.fields.data
        device = form.sensors.data

        query = ''' 
        from(bucket:"{}")
            |> range(start: {}, stop: {})
            |> filter(fn:(r) =>
            r._measurement == "sensorWizether" and
            r._field == "{}" and
            r.device == "{}")
        '''.format(bucket, start, stop, field, device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        client = InfluxDBClient(url=url, token=token, org=org, debug=False)
        df_result = client.query_api().query_data_frame(org=org, query=query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)
        if df_result.empty:
            flash('No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            # Remove useless cols
            df_result = df_result.drop(columns=['result', 'table', '_start', '_stop', '_measurement'])
            df_result = df_result.rename(columns={'_time': 'time', '_value': 'value', '_field': 'field'})
            
            df_result.to_csv(filename_path, index = False)

        return send_file(filename_path, as_attachment=True) 
    else:
        flash('Error. Revisa los datos introducidos y vuelve a probar.')
        return redirect(url_for('dashboard.open_api'))

@api_bp.route('/query_all_date_range', methods=['POST'])
@login_required
def query_date_range_all():

    token = app.config['INFLUX_TOKEN']
    org = app.config['INFLUX_ORG']
    bucket = app.config['INFLUX_BUCKET']
    url = app.config['INFLUX_URL']

    form = QueryAPI_DateRange_All(request.form)
    if form.validate_on_submit():
        start = form.start_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        stop = form.stop_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        device = form.sensors.data

        query = ''' 
        from(bucket:"{}")
            |> range(start: {}, stop: {})
            |> filter(fn:(r) =>
            r._measurement == "sensorWizether" and
            r.device == "{}")
        '''.format(bucket, start, stop, device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        client = InfluxDBClient(url=url, token=token, org=org, debug=False)
        df_result = client.query_api().query_data_frame(org=org, query=query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)
        if df_result.empty:
            flash('No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            # Remove useless cols
            df_result = df_result.drop(columns=['result', 'table', '_start', '_stop', '_measurement'])
            df_result = df_result.rename(columns={'_time': 'time', '_value': 'value', '_field': 'field'})
            print(df_result.head())
            df_result.to_csv(filename_path, index = False)

        return send_file(filename_path, as_attachment=True) 
    else:
        flash('Error. Revisa los datos introducidos y vuelve a probar.')
        return redirect(url_for('dashboard.open_api'))


#
# Tasks
#

# Task view
@api_bp.route('/tasks/', methods=['GET'])
@login_required
def gettasks():
    queue = Queue()
    error = []
    try:
        jobs = queue.jobs
    except Exception as ex:
        error.append(str(ex))
        # print(ex)
        return render_template('dashboard/tasks.html',
                               error_list=error,
                               user=current_user)

    return render_template('dashboard/tasks.html',
                           jobs=jobs,
                           error_list=error,
                           user=current_user)


# Enqueue Task
@api_bp.route('/enqueue_task/<task_name>', methods=['GET', 'POST'])
@login_required
def enqueue_task(task_name):
    app.logger.info("Enqueuing task " + task_name)

    queue = Queue(default_timeout=3600)

    # Running a function (inside tasks.py) by its name
    # This is either pure genius or a massive hack
    task = queue.enqueue(getattr(tasks, task_name), result_ttl=1000)

    app.logger.info("Task enqueued. Currently " + str(len(queue)) + " tasks in queue.")

    return jsonify({}), 202, {
        'Location':
        url_for('api.job_status',
                _external=True,
                _scheme='https',
                job_id=task.get_id())
    }


# Query Job Status. Finding the result of a Job
@api_bp.route('/status/<job_id>')
@login_required
def job_status(job_id):
    queue = Queue()
    job = queue.fetch_job(job_id)
    if job is None:
        response = {'status': 'unknow'}
    else:
        print(job.to_dict())
        response = {
            'status': job.get_status(),
            'result': str(job.result)
        }

        if job.is_failed:
            response['message'] = job.exc_info.strip().split('\n')[-1]

        app.logger.info(response)

    return jsonify(response)


#
# Getting the redis connection or setup
#
def get_redis_connection():
    redis_connection = getattr(g, '_redis_connection', None)
    if redis_connection is None:
        redis_url = app.config['REDIS_URL']
        redis_connection = g._redis_connection = redis.from_url(redis_url)

    return redis_connection


#
# RQ Management for Redis Queues
#
@api_bp.before_request
def push_rq_connection():
    push_connection(get_redis_connection())


#
# RQ Management for Redis Queues
#
@api_bp.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()
