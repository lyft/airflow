#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Add description column to Variable

Revision ID: b7a8283de53b
Revises: 03afc6b6f902
Create Date: 2023-03-28 22:36:38.354244

"""

# revision identifiers, used by Alembic.
revision = 'b7a8283de53b'
down_revision = '03afc6b6f902'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('variable', sa.Column('description', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('variable', 'description')

