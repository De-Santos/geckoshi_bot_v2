"""update TaskType

Revision ID: ac34784c2a4a
Revises: bf0dae1f651b
Create Date: 2024-08-22 03:31:34.275394

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = 'ac34784c2a4a'
down_revision: Union[str, None] = 'bf0dae1f651b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Use a raw SQL statement to check if the enum type already exists
    conn = op.get_bind()
    result = conn.execute(text("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname = 'tasktype');"))
    exists = result.scalar()

    if not exists:
        # Create the enum type if it doesn't exist
        enum_type = ENUM('TIME_BASED', 'DONE_BASED', 'POOL_BASED', 'BONUS', name='tasktype')
        enum_type.create(conn, checkfirst=False)
    else:
        # If the type exists, add the new value
        conn.execute(text("ALTER TYPE tasktype ADD VALUE 'BONUS';"))


def downgrade():
    # Enum types are difficult to downgrade without dropping the type entirely
    # This is not typically recommended, but if necessary:
    conn = op.get_bind()
    conn.execute("DELETE FROM pg_enum WHERE enumlabel = 'BONUS' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'tasktype');")
