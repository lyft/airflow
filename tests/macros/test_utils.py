from mock import patch
import os
import unittest

from airflow.macros import s3_location


class TestUtils(unittest.TestCase):

    @patch.dict(os.environ, {'SERVICE_INSTANCE': 'development'})
    def test_s3_location_in_local(self):
        assert s3_location('test_schema', 'test_table') == 'file:/tmp/hive-warehouse/' \
                                                           'PRODUCTION/test_schema/test_table'

    @patch.dict(os.environ, {'SERVICE_INSTANCE': 'production'})
    def test_s3_location_in_prod(self, ):
        assert s3_location('test_schema', 'test_table') == 's3://lyftqubole-iad/qubole/t/stfihs/' \
                                                           'PRODUCTION/{schema}/table_name={table}'\
            .format(schema='test_schema',
                    table='test_table')

    @patch.dict(os.environ, {'SERVICE_INSTANCE': 'production'})
    def test_s3_location_for_intermediate_table(self):
        assert s3_location('test_schema', 'test_table', is_dest=False) \
            == 's3://lyftqubole-iad/qubole/t/stfihs/' \
               'PRODUCTION/{schema}/table_name={table}_{{ ds_nodash }}'\
            .format(schema='test_schema',
                    table='test_table')