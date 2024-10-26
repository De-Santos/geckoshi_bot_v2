from typing import Set

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import make_transient

from database import Cheque, with_session, now, TransactionOperation
from transaction_manager import make_transaction_from_system, generate_trace, TraceType


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
        await make_transaction_from_system(
            target=self.entity.created_by_id,
            operation=TransactionOperation.INCREMENT,
            amount=self.entity.amount,
            created_by=initiator,
            description='cheque amount allocation rollback',
            trace=generate_trace(TraceType.CHEQUE, str(self.entity.trace_uuid)),
            session=s,
            currency_type=self.entity.currency_type,
            auto_commited=False
        )

        stmt = (update(Cheque)
                .where(Cheque.id.__eq__(self.entity.id))
                .values(deleted_by_id=initiator, deleted_at=now()))
        await s.execute(stmt)

    @with_session
    async def update_cheque(self, s: AsyncSession = None, **kwargs) -> None:
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
