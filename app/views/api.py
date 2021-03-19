from flask import Blueprint, render_template, request, redirect, jsonify, url_for, g, send_file, current_app, flash
from flask import current_app as app
from flask_login import login_required, current_user
from rq import push_connection, pop_connection, Queue
import redis

from datetime import datetime
from pathlib import Path
import pandas as pd
import os

from app import tasks
from app.influx import sendQueryInflux, removeUselessColumns
from app.forms import *

api_bp = Blueprint('api', __name__, url_prefix='/api')

#
# Open API
#

@api_bp.route('/query_date_range', methods=['POST'])
@login_required
def query_date_range():

    form = QueryAPI_DateRange_Field(request.form)
    if form.validate_on_submit():
        start = form.start_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        stop = form.stop_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        field = form.fields.data
        device = form.sensors.data

        # Check if start date its wrong
        if(start > stop):
            flash('Error. La fecha de inicio no puede ser mayor a la fecha de fin.')
            return redirect(url_for('dashboard.open_api'))

        query = ''' 
        from(bucket:"{}")
            |> range(start: {}, stop: {})
            |> filter(fn:(r) =>
            r._measurement == "sensorWizether" and
            r._field == "{}" and
            r.device == "{}")
        '''.format(app.config['INFLUX_BUCKET'], start, stop, field, device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        df_result = sendQueryInflux(query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)
        
        if df_result.empty:
            flash('Error. No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            df_result = removeUselessColumns(df_result)
            df_result.to_csv(filename_path, index = False)

        return send_file(filename_path, as_attachment=True) 
    else:
        flash('Error. Revisa los datos introducidos y vuelve a probar.')
        return redirect(url_for('dashboard.open_api'))


@api_bp.route('/query_all_date_range', methods=['POST'])
@login_required
def query_date_range_all():

    form = QueryAPI_DateRange_All(request.form)
    if form.validate_on_submit():
        start = form.start_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        stop = form.stop_date.data.strftime("%Y-%m-%dT%H:%M:%SZ")
        device = form.sensors.data

        # Check if start date its wrong
        if(start > stop):
            flash('Error. La fecha de inicio no puede ser mayor a la fecha de fin.')
            return redirect(url_for('dashboard.open_api'))

        query = ''' 
        from(bucket:"{}")
            |> range(start: {}, stop: {})
            |> filter(fn:(r) =>
            r._measurement == "sensorWizether" and
            r.device == "{}")
        '''.format(app.config['INFLUX_BUCKET'], start, stop, device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        df_result = sendQueryInflux(query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)

        if df_result.empty:
            flash('Error. No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            # Remove useless cols
            df_result = removeUselessColumns(df_result)
            df_result.to_csv(filename_path, index = False)

        return send_file(filename_path, as_attachment=True) 
    else:
        flash('Error. Revisa los datos introducidos y vuelve a probar.')
        return redirect(url_for('dashboard.open_api'))

@api_bp.route('/query_history_device', methods=['POST'])
@login_required
def query_history_device():

    form = QueryAPI_history_device(request.form)
    if form.validate_on_submit():
        device = form.sensors.data

        query = ''' 
            from(bucket:"{}")
                |> range(start: 2021-03-01T00:00:00Z, stop: now())
                |> filter(fn:(r) =>
                r._measurement == "sensorWizether" and
                r.device == "{}")
        '''.format(app.config['INFLUX_BUCKET'], device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        df_result = sendQueryInflux(query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)

        if df_result.empty:
            flash('Error. No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            df_result = removeUselessColumns(df_result)
            df_result.to_csv(filename_path, index = False)

        return send_file(filename_path, as_attachment=True) 
    else:
        flash('Error. Revisa los datos introducidos y vuelve a probar.')
        return redirect(url_for('dashboard.open_api'))


@api_bp.route('/query_lastweek_device', methods=['POST'])
@login_required
def query_lastweek_device():

    form = QueryAPI_lastweek_device(request.form)
    if form.validate_on_submit():
        device = form.sensors.data

        query = ''' 
            from(bucket:"{}")
                |> range(start: -7d, stop: now())
                |> filter(fn:(r) =>
                r._measurement == "sensorWizether" and
                r.device == "{}")
        '''.format(app.config['INFLUX_BUCKET'], device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        df_result = sendQueryInflux(query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)

        if df_result.empty:
            flash('Error. No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            df_result = removeUselessColumns(df_result)
            df_result.to_csv(filename_path, index = False)

        return send_file(filename_path, as_attachment=True) 
    else:
        flash('Error. Revisa los datos introducidos y vuelve a probar.')
        return redirect(url_for('dashboard.open_api'))


@api_bp.route('/query_lastweek_device_max', methods=['POST'])
@login_required
def query_lastweek_device_max():

    form = QueryAPI_lastweek_device_max(request.form)
    if form.validate_on_submit():
        device = form.sensors.data

        query = ''' 
            from(bucket:"{}")
                |> range(start: -7d, stop: now())
                |> filter(fn:(r) =>
                r._measurement == "sensorWizether" and
                r.device == "{}")
                |> max()
        '''.format(app.config['INFLUX_BUCKET'], device)

        #print(query)

        root_path = Path(current_app.root_path).parent
        upload_path = os.path.join(root_path, 'api_tmp')

        df_result = sendQueryInflux(query)

        filename = 'data_' + datetime.now().strftime("%Y-%m-%d") + '.csv'
        filename_path = os.path.join(upload_path, filename)

        if df_result.empty:
            flash('Error. No se han encontrado datos')
            return redirect(url_for('dashboard.open_api'))
        else:
            df_result = removeUselessColumns(df_result)
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
