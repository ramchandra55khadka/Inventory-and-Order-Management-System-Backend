"""initial tables

Revision ID: 20260111_0001
Revises: 
Create Date: 2026-01-11 09:10:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260111_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, index=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("customer_name", sa.String, index=True),
        sa.Column("status", sa.String, default="confirmed"),
        sa.Column("total_amount", sa.Float),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id")),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id")),
        sa.Column("unit_price", sa.Float),
        sa.Column("quantity", sa.Integer),
        sa.Column("line_total", sa.Float),
    )


def downgrade():
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("items")
