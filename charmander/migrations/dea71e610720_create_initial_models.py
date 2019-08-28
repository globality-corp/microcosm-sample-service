"""
Create Initial Models

Revision ID: dea71e610720
Revises: e107ab9eb193
Create Date: 2019-08-28 12:33:23.992504

"""
import sqlalchemy as sa
from alembic import op
from microcosm_postgres.models import UTCDateTime
from microcosm_postgres.types import EnumType, Serial
from sqlalchemy import (
    CheckConstraint,
    Column,
    FetchedValue,
    Float,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import UUIDType

from charmander.enums import Purpose, Resolution
from charmander.models.order_event_type import OrderEventType
from charmander.models.pizza_model import CrustType, PizzaSize
from charmander.models.topping_model import ToppingType


# revision identifiers, used by Alembic.
revision = "dea71e610720"
down_revision = "e107ab9eb193"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "order",
        Column("id", UUIDType(), nullable=False),
        Column("created_at", Float(), nullable=False),
        Column("updated_at", Float(), nullable=False),
        Column("customer_id", UUIDType(), nullable=False),
        Column("purpose", EnumType(Purpose), nullable=False),
        Column("resolution", EnumType(Resolution), nullable=False),
        PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "order_event",
        Column("id", UUIDType(), nullable=False),
        Column("created_at", Float(), nullable=False),
        Column("updated_at", Float(), nullable=False),
        Column("customer_id", UUIDType(), nullable=False),
        Column("pizza_size", EnumType(PizzaSize), nullable=True),
        Column("crust_type", EnumType(CrustType), nullable=True),
        Column("topping_type", EnumType(ToppingType), nullable=True),
        Column("purpose", EnumType(Purpose), nullable=False),
        Column("resolution", EnumType(Resolution), nullable=False),
        Column("order_id", UUIDType(), nullable=False),
        # Notice these columns which aren't explicitly defined in the model,
        # But are added automatically from the base class
        Column("event_type", EnumType(OrderEventType), nullable=False),
        Column("clock",Serial(), server_default=FetchedValue(), nullable=False),
        Column("parent_id", UUIDType(), nullable=True),
        Column("state", ARRAY(EnumType(OrderEventType)), nullable=False),
        Column("version", Integer(), nullable=False),
        CheckConstraint(
            "crust_type IS NOT NULL OR event_type NOT IN ('PizzaCreated')",
            name="require_order_event_crust_type",
        ),
        CheckConstraint(
            "customer_id IS NOT NULL OR event_type NOT IN ('OrderInitialized')",
            name="require_order_event_customer_id",
        ),
        CheckConstraint(
            "parent_id IS NOT NULL OR (version = 1 AND event_type IN ('OrderInitialized'))",
            name="require_order_event_parent_id",
        ),
        CheckConstraint(
            "pizza_size IS NOT NULL OR event_type NOT IN ('PizzaCreated')",
            name="require_order_event_pizza_size",
        ),
        CheckConstraint(
            "topping_type IS NOT NULL OR event_type NOT IN ('PizzaToppingAdded')",
            name="require_order_event_topping_type",
        ),
        ForeignKeyConstraint(
            ["order_id"],
            ["order.id"],
        ),
        ForeignKeyConstraint(
            ["parent_id"],
            ["order_event.id"],
        ),
        PrimaryKeyConstraint("id"),
        UniqueConstraint("clock"),
        UniqueConstraint("parent_id")
    )
    op.create_index("order_event_unique_logical_clock", "order_event", ["order_id", "clock"], unique=True)
    op.create_table(
        "topping",
        Column("id", UUIDType(), nullable=False),
        Column("created_at", UTCDateTime(), nullable=False),
        Column("updated_at", UTCDateTime(), nullable=False),
        Column("pizza_id", UUIDType(), nullable=False),
        Column("topping_type", EnumType(ToppingType), nullable=False),
        ForeignKeyConstraint(
            ["pizza_id"],
            ["pizza.id"],
        ),
        PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("topping")
    op.drop_index("order_event_unique_logical_clock", table_name="order_event")
    op.drop_table("order_event")
    op.drop_table("order")
