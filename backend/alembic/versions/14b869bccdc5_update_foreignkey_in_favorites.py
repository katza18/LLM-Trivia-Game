"""Update ForeignKey in favorites

Revision ID: 14b869bccdc5
Revises: 9216bbe45943
Create Date: 2025-04-24 10:14:48.849432

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14b869bccdc5'
down_revision: Union[str, None] = '9216bbe45943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_question_favorite', 'questions', ['question_id'], ['id']
        )
        batch_op.create_foreign_key(
            'fk_user_favorite', 'users', ['user_id'], ['id']
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
    # ### end Alembic commands ###
