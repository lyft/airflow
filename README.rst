
.. Licensed to the Apache Software Foundation (ASF) under one
   or more contributor license agreements.  See the NOTICE file
   distributed with this work for additional information
   regarding copyright ownership.  The ASF licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

..   http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.


Package ``apache-airflow-providers-ssh``

Release: ``1.2.0``


`Secure Shell (SSH) <https://tools.ietf.org/html/rfc4251>`__


Provider package
================

This is a provider package for ``ssh`` provider. All classes for this provider package
are in ``airflow.providers.ssh`` python package.

You can find package information and changelog for the provider
in the `documentation <https://airflow.apache.org/docs/apache-airflow-providers-ssh/1.2.0/>`_.


Installation
============

NOTE!

On November 2020, new version of PIP (20.3) has been released with a new, 2020 resolver. This resolver
does not yet work with Apache Airflow and might lead to errors in installation - depends on your choice
of extras. In order to install Airflow you need to either downgrade pip to version 20.2.4
``pip install --upgrade pip==20.2.4`` or, in case you use Pip 20.3, you need to add option
``--use-deprecated legacy-resolver`` to your pip install command.

You can install this package on top of an existing airflow 2.* installation via
``pip install apache-airflow-providers-ssh``

PIP requirements
================

=============  ==================
PIP package    Version required
=============  ==================
``paramiko``   ``>=2.6.0``
``pysftp``     ``>=0.2.9``
``sshtunnel``  ``>=0.1.4,<0.2``
=============  ==================