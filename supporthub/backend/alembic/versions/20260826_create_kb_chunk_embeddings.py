"""Create kb_chunk_embeddings table for RAG pgvector embeddings

Revision ID: 20260826_kb_chunks
Revises: 20260804_add_external_message_id
Create Date: 2026-08-26 14:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision = '20260826_kb_chunks'
down_revision = '20260804_add_external_message_id'

branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.create_table(
        'kb_chunk_embeddings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('chunk_id', sa.String(length=255), nullable=False),
        sa.Column('source_id', sa.String(length=255), nullable=False),
        sa.Column('source_type', sa.String(length=100), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', Vector(768), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chunk_id')
    )
    op.create_index('ix_kb_chunk_embeddings_chunk_id', 'kb_chunk_embeddings', ['chunk_id'], unique=True)
    op.create_index('ix_kb_chunk_embeddings_source_id', 'kb_chunk_embeddings', ['source_id'], unique=False)
    op.create_index('ix_kb_chunk_embeddings_category', 'kb_chunk_embeddings', ['category'], unique=False)

    # HNSW Index for fast cosine similarity search on 768-dim vectors
    op.execute(
        "CREATE INDEX ix_kb_chunk_embeddings_vector ON kb_chunk_embeddings USING hnsw (embedding vector_cosine_ops);"
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_kb_chunk_embeddings_vector;")
    op.drop_index('ix_kb_chunk_embeddings_category', table_name='kb_chunk_embeddings')
    op.drop_index('ix_kb_chunk_embeddings_source_id', table_name='kb_chunk_embeddings')
    op.drop_index('ix_kb_chunk_embeddings_chunk_id', table_name='kb_chunk_embeddings')
    op.drop_table('kb_chunk_embeddings')
