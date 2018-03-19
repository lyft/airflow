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
#
"""
Utilities module for cli
"""
from __future__ import absolute_import
import functools
from datetime import datetime
import sys
import os

import airflow.models
from airflow.utils import action_loggers


def action_logging(f):
    """
    Decorates function to execute function at the same time submitting action_logging but in CLI context
    :param f: function instance
    :return: wrapped function
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        metrics = _build_metrics(f.__name__, *args)

        try:
            result = f(*args, **kwargs)
        except:
            metrics['error'] = sys.exc_info()[1]
        finally:
            metrics['end_datetime'] = datetime.utcnow()
            try:
                action_loggers.submit(**metrics)
            finally:
                return result
    return wrapper


def _build_metrics(func_name, *args):
    """
    Builds metrics dict from function args
    :param func_name: name of function
    :param args: args
    :return: dict with metrics
    """
    metrics = {'event': func_name}
    metrics['start_datetime'] = datetime.utcnow()
    metrics['full_command'] = str(list(sys.argv))
    metrics['user'] = os.environ.get('USER')

    print "args[0]: {}".format(args[0])
    if args:
        tmp_dic = vars(args[0])
        metrics['dag_id'] = tmp_dic.get('dag_id')
        metrics['task_id'] = tmp_dic.get('task_id')
        metrics['execution_date'] = tmp_dic.get('execution_date')

    log = airflow.models.Log(
        event=func_name,
        task_instance=None,
        owner=metrics['user'],
        extra=str(metrics['full_command']),
        task_id=metrics.get('task_id'),
        dag_id=metrics.get('dag_id'),
        execution_date=metrics.get('execution_date'))
    metrics['log'] = log
    return metrics
