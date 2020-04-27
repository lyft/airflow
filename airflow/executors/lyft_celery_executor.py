# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from airflow.exceptions import AirflowException
from airflow.executors.celery_executor import (
    app,
    celery_states,
    CeleryExecutor,
    DEFAULT_QUEUE,
)
from typing import Dict

import json
import logging
import subprocess
import os

from airflow.models import Variable

CONFIDANT_JSON_FILE = '/dev/shm/confidant/confidant_data'

def refresh_env_from_confidant():
    # type: () -> Dict[str, str]
    env = os.environ.copy()
    with open(CONFIDANT_JSON_FILE, 'r') as f:
        confidant_creds = json.load(f)['credentials']
        for (key, value) in confidant_creds.items():
            env['CREDENTIALS_{}'.format(key.upper())] = value

    return env

@app.task
def execute_command_with_fresh_creds(command):
    """
    See execute_command() from celery_executor.py
    """
    logging.info("Executing command in Celery " + command)
    try:
        output = subprocess.check_output(
            command,
            shell=True,
            env=refresh_env_from_confidant(),
            close_fds=True,
            stderr=subprocess.STDOUT,
        )
        logging.info(output)
    except subprocess.CalledProcessError as e:
        logging.exception('execute_command encountered a CalledProcessError')
        logging.error(e.output)
        raise AirflowException('Celery command failed')


class LyftCeleryExecutor(CeleryExecutor):
    """
    Exactly like the CeleryExecutor, except that it refreshes
    environment variables with the latest Confidant credentials before
    launching the subprocess corresponding to each task.
    """

    def __init__(self):
        super(LyftCeleryExecutor, self).__init__()
        self.py3_dag_id_whitelist = {
            'engdocs_page_views'
        }

    def execute_async(self, key, command, queue=DEFAULT_QUEUE):
        self.logger.info("[celery] queuing {key} through celery, "
                         "queue={queue}".format(**locals()))

        try:
            # key is a tuple and here is an example:
            # (u'dag_gschema_data_compactor', u'zippy_partition_issue_redrive_event_gschema_route_v3',
            #   datetime.datetime(2020, 4, 27, 21, 15))
            dag_id = key[0]
            if dag_id in self.py3_dag_id_whitelist:
                queue = 'py3'
        except Exception as e:
            self.logger.error('Failing to do queue routing because of {e}'.format(e=str(e)))

        self.tasks[key] = execute_command_with_fresh_creds.apply_async(
            args=[command], queue=queue)
        self.last_state[key] = celery_states.PENDING
