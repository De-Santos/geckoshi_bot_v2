"""add default inserts in settings

Revision ID: cef8ae637aca
Revises: 443583ea0db6
Create Date: 2024-09-01 01:48:09.270983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cef8ae637aca'
down_revision: Union[str, None] = '443583ea0db6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    settings_to_insert = [
        ('MIN_WITHDRAW_IN_AIRDROP', '0', None),
        ('PREMIUM_GMEME_PRICE', '30000', None),
        ('PAY_FOR_REFERRAL', '1000', None)
    ]

    for setting_id, int_val, str_val in settings_to_insert:
        connection.execute(
            sa.text(
                """
                INSERT INTO public.settings (id, int_val, str_val)
                SELECT :id, :int_val, :str_val
                WHERE NOT EXISTS (
                    SELECT 1 FROM public.settings WHERE id = :id
                );
                """
            ),
            parameters={'id': setting_id, 'int_val': int_val, 'str_val': str_val},
        )


def downgrade() -> None:
    pass
