from copy import deepcopy

from pydantic import BaseModel, Field
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from database import Cheque, with_session, now


class ChequeModifier(BaseModel):
    entity: Cheque = Field()

    def __init__(self, **data):
        if 'entity' in data:
            data['entity'] = deepcopy(data['entity'])
        super().__init__(**data)

    @with_session
    async def link_user(self, user_id: int, s: AsyncSession = None) -> None:
        stmt = (
            update(Cheque)
            .where(Cheque.id.__eq__(self.entity.id))
            .values(connected_to_user=user_id)
            .returning(Cheque)
        )

        result = await s.execute(stmt)
        updated_cheque = result.scalar_one_or_none()

        if updated_cheque is None:
            raise ValueError(f"No cheque found with id {self.entity.id} to update.")

        self.entity = deepcopy(updated_cheque)

    @with_session
    async def update_description(self, description: str, s: AsyncSession = None) -> None:
        stmt = (
            update(Cheque)
            .where(Cheque.id.__eq__(self.entity.id))
            .values(description=description)
            .returning(Cheque)
        )

        result = await s.execute(stmt)
        updated_cheque = result.scalar_one_or_none()

        if updated_cheque is None:
            raise ValueError(f"No cheque found with id {self.entity.id} to update.")

        self.entity = deepcopy(updated_cheque)

    @with_session
    async def delete_cheque(self, initiator: int, s: AsyncSession = None) -> None:
        stmt = (update(Cheque)
                .where(Cheque.id.__eq__(self.entity.id))
                .values(deleted_by_id=initiator, deleted_at=now()))
        await s.execute(stmt)

    class Config:
        arbitrary_types_allowed = True


__all__ = [
    'ChequeModifier'
]
