"""Add external_message_id to messages table

Revision ID: 20260804_add_external_message_id
Revises: 
Create Date: 2026-08-04 14:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260804_add_external_message_id'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('messages', sa.Column('external_message_id', sa.String(length=255), nullable=True))
    op.create_index('ix_messages_external_message_id', 'messages', ['external_message_id'], unique=False)


def downgrade():
    op.drop_index('ix_messages_external_message_id', table_name='messages')
    op.drop_column('messages', 'external_message_id')
