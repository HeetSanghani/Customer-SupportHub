"""Create ticket_embeddings table for pgvector similar ticket search

Revision ID: 20260827_ticket_embeddings
Revises: 20260826_kb_chunks
Create Date: 2026-08-27 11:48:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision = '20260827_ticket_embeddings'
down_revision = '20260826_kb_chunks'

branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.create_table(
        'ticket_embeddings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ticket_id', sa.UUID(), nullable=False),
        sa.Column('embedding', Vector(768), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticket_id')
    )
    op.create_index('ix_ticket_embeddings_ticket_id', 'ticket_embeddings', ['ticket_id'], unique=True)

    # HNSW Index for fast cosine similarity search on 768-dim ticket embeddings
    op.execute(
        "CREATE INDEX ix_ticket_embeddings_vector ON ticket_embeddings USING hnsw (embedding vector_cosine_ops);"
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_ticket_embeddings_vector;")
    op.drop_index('ix_ticket_embeddings_ticket_id', table_name='ticket_embeddings')
    op.drop_table('ticket_embeddings')
