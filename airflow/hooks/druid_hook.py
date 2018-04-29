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

from __future__ import print_function

from contextlib import closing
import requests
import sys
import time

from pydruid.db import connect
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class DruidHook(BaseHook):
    """
    Connection to Druid

    :param druid_ingest_conn_id: The connection id to the Druid overlord machine which accepts index jobs
    :type druid_ingest_conn_id: string
    :param timeout: The interval between polling the Druid job for the status of the ingestion job
    :type timeout: int
    :param max_ingestion_time: The maximum ingestion time before assuming the job failed
    :type max_ingestion_time: int
    :param druid_broker_conn_id: The connection id to the Druid broker machine
    :type druid_broker_conn_id: string
    """
    def __init__(
            self,
            druid_ingest_conn_id='druid_ingest_default',
            timeout=1,
            max_ingestion_time=None,
            druid_broker_conn_id='druid_broker_default'):

        self.druid_ingest_conn_id = druid_ingest_conn_id
        self.druid_broker_conn_id = druid_broker_conn_id
        self.timeout = timeout
        self.max_ingestion_time = max_ingestion_time
        self.header = {'content-type': 'application/json'}

    def get_conn_url(self):
        conn = self.get_connection(self.druid_ingest_conn_id)
        host = conn.host
        port = conn.port
        schema = conn.extra_dejson.get('schema', 'http')
        endpoint = conn.extra_dejson.get('endpoint', '')
        return "http://{host}:{port}/{endpoint}".format(**locals())

    def get_broker_conn(self):
        conn = self.get_connection(self.druid_broker_conn_id)
        druid_broker_conn = connect(
            host=conn.host,
            port=conn.port,
            path=conn.extra_dejson.get('endpoint', '/druid/v2/sql'),
            scheme=conn.extra_dejson.get('schema', 'http')
        )
        return druid_broker_conn

    def submit_indexing_job(self, json_index_spec):
        url = self.get_conn_url()

        req_index = requests.post(url, data=json_index_spec, headers=self.header)
        if (req_index.status_code != 200):
            raise AirflowException("Did not get 200 when submitting the Druid job to {}".format(url))

        req_json = req_index.json()
        # Wait until the job is completed
        druid_task_id = req_json['task']

        running = True

        sec = 0
        while running:
            req_status = requests.get("{0}/{1}/status".format(url, druid_task_id))

            self.log.info("Job still running for %s seconds...", sec)

            sec = sec + 1

            if self.max_ingestion_time and sec > self.max_ingestion_time:
                # ensure that the job gets killed if the max ingestion time is exceeded
                requests.post("{0}/{1}/shutdown".format(url, druid_task_id))
                raise AirflowException('Druid ingestion took more than %s seconds', self.max_ingestion_time)

            time.sleep(self.timeout)

            status = req_status.json()['status']['status']
            if status == 'RUNNING':
                running = True
            elif status == 'SUCCESS':
                running = False  # Great success!
            elif status == 'FAILED':
                raise AirflowException('Druid indexing job failed, check console for more info')
            else:
                raise AirflowException('Could not get status of the job, got %s', status)

        self.log.info('Successful index')

    def get_first(self, sql, parameters=None):
        """
        Executes the druid sql to druid broker and returns the first resulting row.

        :param sql: the sql statement to be executed (str)
        :type sql: str
        :param parameters: The parameters to render the SQL query with.
        :type parameters: mapping or iterable
        """
        if sys.version_info[0] < 3:
            sql = sql.encode('utf-8')

        with closing(self.get_broker_conn()) as conn:
            with closing(conn.cursor()) as cur:
                if parameters is not None:
                    cur.execute(sql, parameters)
                else:
                    cur.execute(sql)
                return cur.fetchone()

    def get_records(self, sql, parameters=None):
        """
        Executes the druid sql to druid broker and returns a set of records.

        :param sql: the sql statement to be executed (str).
        :type sql: str
        :param parameters: The parameters to render the SQL query with.
        :type parameters: mapping or iterable
        """
        if sys.version_info[0] < 3:
            sql = sql.encode('utf-8')

        with closing(self.get_broker_conn()) as conn:
            with closing(conn.cursor()) as cur:
                if parameters is not None:
                    cur.execute(sql, parameters)
                else:
                    cur.execute(sql)
                return cur.fetchall()
