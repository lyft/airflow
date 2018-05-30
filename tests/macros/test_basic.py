import unittest

from airflow.macros import update_params
from airflow.models import DagRun


class BasicMacrosTests(unittest.TestCase):
    def test_update_params(self):
        dag_run = DagRun()
        dag_run.conf = {"overridden": True}
        params = {"overridden": False}

        update_params(params, dag_run)

        self.assertEqual(True, params["overridden"])

    def test_update_params_dag_run_is_none(self):
        params = {"overridden": False}

        update_params(params, None)

        self.assertEqual(False, params["overridden"])

    def test_update_params_conf_is_none(self):
        dag_run = DagRun()
        params = {"overridden": False}

        update_params(params, dag_run)

        self.assertEqual(False, params["overridden"])
