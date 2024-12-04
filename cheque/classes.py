from decimal import Decimal
from typing import Set

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import make_transient

from database import Cheque, with_session, now, get_cheque_activations_count


class ChequeModifier:
    ALLOWED_UPDATE_FIELDS: Set = {
        Cheque.name,
        Cheque.description,
        Cheque.connected_to_user,
    }

    def __init__(self, entity: Cheque):
        if isinstance(entity, Cheque):
            make_transient(entity)  # Detaches from the session
            self.entity = entity
        else:
            raise TypeError('entity must be Cheque type')

    def __update_entity(self, entity: Cheque):
        make_transient(entity)
        self.entity = entity

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

        self.__update_entity(updated_cheque)

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

        self.__update_entity(updated_cheque)

    @with_session
    async def delete_cheque(self, initiator: int, s: AsyncSession = None) -> None:
        stmt = (update(Cheque)
                .where(Cheque.id.__eq__(self.entity.id))
                .values(deleted_by_id=initiator, deleted_at=now())
                .returning(Cheque))

        result = await s.execute(stmt)
        updated_cheque = result.scalar_one_or_none()
        self.__update_entity(updated_cheque)

    @with_session
    async def get_activated_amount(self, s: AsyncSession = None) -> Decimal:
        activations_count = await get_cheque_activations_count(self.entity.id, s=s)
        return self.get_per_user_amount() * activations_count

    def get_per_user_amount(self) -> Decimal:
        return self.entity.amount / self.entity.activation_limit

    @with_session
    async def update(self, s: AsyncSession = None, unsafe: bool = False, **kwargs) -> None:
        if not unsafe:
            self.__validate_update(**kwargs)

        stmt = (update(Cheque)
                .where(Cheque.id.__eq__(self.entity.id))
                .values(**kwargs)
                .returning(Cheque))

        result = await s.execute(stmt)
        updated_cheque = result.scalar_one_or_none()

        if updated_cheque is None:
            raise ValueError(f"No cheque found with id {self.entity.id} to update.")

        self.__update_entity(updated_cheque)

    def __validate_update(self, **kwargs) -> None:
        allowed_field_names = {field.name for field in self.ALLOWED_UPDATE_FIELDS}
        unsupported_fields = [field for field in kwargs if field not in allowed_field_names]
        if unsupported_fields:
            raise ValueError(f"Unsupported fields for update: {', '.join(unsupported_fields)}")

    def is_creator(self, user_id: int) -> bool:
        return self.entity.created_by_id == user_id

    def is_connected_to_user(self, user_id: int) -> bool:
        if self.entity.connected_to_user is None:
            return True
        return self.entity.connected_to_user == user_id

    class Config:
        arbitrary_types_allowed = True


__all__ = [
    'ChequeModifier'
]
