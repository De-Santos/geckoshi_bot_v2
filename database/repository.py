import logging
import uuid
from datetime import datetime, date
from typing import Any, Sequence, Union, Optional

from sqlalchemy import and_, or_, func, union, text
from sqlalchemy import select, desc, Row, update, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import coalesce

import cache
from database import User, Setting, SettingsKey, MailingMessageStatus, MailingMessage, Mailing, now, MailingStatus, Task, TaskType, TaskDoneHistory, UserActivityStatistic, CustomClientToken, UserActivityContext, CustomClientTokenType, Cheque, ChequeActivation
from database.decorators import with_session
from lang.lang_based_provider import Lang
from utils.pagination import Pagination

logger = logging.getLogger(__name__)


@with_session
async def get_user_by_tg(tg_user_id: int, s: AsyncSession = None) -> User:
    stmt = select(User).where(User.telegram_id.__eq__(tg_user_id))
    return await s.scalar(stmt)


@cache.cacheable(ttl="10m", save_as_blob=True, function_name_as_id=True)
@with_session
async def get_users_statistic(s: AsyncSession = None):
    start_of_day = datetime.combine(date.today(), datetime.min.time())
    end_of_day = datetime.combine(date.today(), datetime.max.time())

    today_join_stmt = (select(func.count(User.telegram_id))
                       .where(User.created_at.between(start_of_day, end_of_day)))
    total_user_count = (select(func.count(User.telegram_id)))

    union_stmt = union(today_join_stmt, total_user_count)
    join_count, total_count = (await s.execute(union_stmt)).scalars()

    return join_count, total_count


@cache.cacheable(ttl="1h", save_as_blob=True, function_name_as_id=True)
@with_session
async def get_activity_statistic(s: AsyncSession = None):
    stmt = (
        select(
            func.date(UserActivityStatistic.datetime_).label('activity_date'),
            func.count(func.distinct(UserActivityStatistic.user_id))
        )
        .group_by(text('activity_date'))
        .order_by(text('activity_date DESC'))
    )
    result = await s.execute(stmt)
    return reversed(result.all())


@cache.cacheable(ttl="10m", save_as_blob=True, function_name_as_id=True)
@with_session
async def get_dirty_incoming_statistic(s: AsyncSession = None):
    stmt = (
        select(
            func.date(User.created_at).label('joined_date'),
            func.count(User.telegram_id)
        )
        .group_by(text('joined_date'))
        .order_by(text('joined_date DESC'))
        .limit(30)
    )
    result = await s.execute(stmt)
    return reversed(result.all())


@cache.cacheable(ttl="10m", save_as_blob=True, function_name_as_id=True)
@with_session
async def get_incoming_statistic(s: AsyncSession = None):
    stmt = (
        select(
            func.date(User.created_at).label('joined_date'),
            func.count(User.telegram_id)
        )
        .where(User.is_bot_start_completed.__eq__(True))
        .group_by(text('joined_date'))
        .order_by(text('joined_date DESC'))
        .limit(30)
    )
    result = await s.execute(stmt)
    return reversed(result.all())


@with_session
async def get_user_balance(tg_user_id: int, s: AsyncSession = None) -> int:
    stmt = select(User.balance).where(User.telegram_id.__eq__(tg_user_id))
    return await s.scalar(stmt)


@cache.cacheable(ttl="10m")
@with_session
async def is_user_exists_by_tg(tg_user_id: int, s: AsyncSession = None) -> bool:
    stmt = select(User).where(User.telegram_id.__eq__(tg_user_id)).exists().select()
    return await s.scalar(stmt)


@cache.cacheable(ttl="10m")
@with_session
async def has_premium(tg_user_id: int, s: AsyncSession = None) -> bool:
    stmt = select(User.is_premium).where(User.telegram_id.__eq__(tg_user_id))
    result = await s.execute(stmt)
    return result.scalar()


@cache.cacheable(ttl="1m")
@with_session
async def is_good_user_by_tg(tg_user_id: int, s: AsyncSession = None) -> bool:
    ext = select(User) \
        .where(User.telegram_id.__eq__(tg_user_id)) \
        .where(User.blocked.__eq__(False)) \
        .where(User.deleted_at.__eq__(None)) \
        .where(User.is_bot_start_completed.__eq__(True)) \
        .exists() \
        .select()
    result = await s.execute(ext)
    return result.scalar()


@cache.cacheable(ttl="1h")
@with_session
async def is_admin(tg_user_id: int, s: AsyncSession = None) -> bool:
    ext = (select(User)
           .where(User.telegram_id.__eq__(tg_user_id))
           .where(User.is_admin.__eq__(True))
           .exists()
           .select())
    result = await s.execute(ext)
    return result.scalar()


async def save_user(s: AsyncSession, user: User) -> None:
    s.add(user)
    await s.commit()


@with_session
async def update_user_language(tg_user_id: int, lang: Lang, s: AsyncSession = None) -> None:
    await s.begin()
    user = await get_user_by_tg(tg_user_id, s=s)
    user.language = lang
    await s.commit()


@cache.cacheable(associate_none_as=False)
@with_session
async def is_user_admin_by_tg_id(tg_user_id: int, s: AsyncSession = None) -> bool:
    stmt = select(User.is_admin).where(User.telegram_id.__eq__(tg_user_id))
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def get_user_language(tg_user_id: int, s: AsyncSession = None) -> Lang:
    stmt = select(User.language).where(User.telegram_id.__eq__(tg_user_id))
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def update_user_is_bot_start_completed_by_tg_id(tg_user_id: int, val: bool, s: AsyncSession = None) -> None:
    await s.begin()
    user = await get_user_by_tg(tg_user_id, s=s)
    user.is_bot_start_completed = val
    await s.commit()


@with_session
async def get_setting_by_id(key: SettingsKey, s: AsyncSession = None) -> Setting:
    stmt = select(Setting).where(Setting.id.__eq__(key))
    result = await s.execute(stmt)
    return result.scalar()


@cache.cacheable(ttl="20m")
@with_session
async def get_user_referrals_count(tg_user_id: int, s: AsyncSession = None) -> int:
    stmt = select(func.count(User.telegram_id)).where(User.referred_by_id.__eq__(tg_user_id))
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def is_premium_user(tg_user_id: int, s: AsyncSession = None) -> bool:
    stmt = select(User.is_premium).where(User.telegram_id.__eq__(tg_user_id))
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def update_user_premium(tg_user_id: int, premium: bool, s: AsyncSession = None) -> None:
    await s.begin()
    user = await get_user_by_tg(tg_user_id, s=s)
    user.is_premium = premium
    await s.commit()


@cache.cacheable(ttl="6h", function_name_as_id=True)
@with_session
async def get_verified_user_count(s: AsyncSession = None) -> int:
    stmt = (select(func.count())
            .where(User.deleted_at.__eq__(None))
            .where(User.blocked.__eq__(False))
            .where(User.is_bot_start_completed.__eq__(True)))
    return await s.scalar(stmt)


@with_session
async def get_top_users_by_referrals(limit: int = 10, s: AsyncSession = None) -> Sequence[Row[tuple[Any, Any]]]:
    referred_user_alias = User.__table__.alias("referred_user")

    stmt = (
        select(
            User.telegram_id,
            func.count(referred_user_alias.c.telegram_id).label('referral_count')
        )
        .select_from(User)
        .join(referred_user_alias, referred_user_alias.c.referred_by_id == User.telegram_id)
        .group_by(User.telegram_id)
        .order_by(desc('referral_count'))
        .limit(limit)
    )
    result = (await s.execute(stmt)).all()
    return result


@with_session
async def get_top_users_by_referrals_with_start_date(start_date: datetime, limit: int = 10, s: AsyncSession = None) -> Sequence[Row[tuple[Any, Any]]]:
    referred_user_alias = User.__table__.alias("referred_user")

    stmt = (
        select(
            User.telegram_id,
            func.count(referred_user_alias.c.telegram_id).label('referral_count')
        )
        .select_from(User)
        .join(referred_user_alias,
              (referred_user_alias.c.referred_by_id == User.telegram_id) &
              (referred_user_alias.c.created_at >= start_date))
        .group_by(User.telegram_id)
        .order_by(desc('referral_count'))
        .limit(limit)
    )
    result = (await s.execute(stmt)).all()
    return result


@with_session
async def update_mailing_message_status(id_: uuid.UUID, status: MailingMessageStatus, s: AsyncSession = None) -> bool:
    try:
        await s.begin()
        stmt = (
            update(MailingMessage)
            .where(MailingMessage.id.__eq__(id_))
            .values(status=status)
        )
        await s.execute(stmt)
        await s.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to update status for MailingMessage with ID {id_}: {e}")
        return False
    finally:
        await s.close()


@with_session
async def update_mailing_message_statuses_by_mailing_id(mailing_id: int, status: MailingMessageStatus, s: AsyncSession = None) -> bool:
    try:
        await s.begin()
        stmt = (
            update(MailingMessage)
            .where(MailingMessage.mailing_id.__eq__(mailing_id))
            .values(status=status)
        )
        await s.execute(stmt)
        await s.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to update statuses for MailingMessage with mailing_id {mailing_id}: {e}")
        return False
    finally:
        await s.close()


@with_session
async def get_mailing_message(id_: uuid.UUID, s: AsyncSession = None) -> MailingMessage:
    stmt = (select(MailingMessage)
            .where(MailingMessage.id.__eq__(id_)))
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def get_mailing(id_: int, s: AsyncSession = None) -> Mailing:
    stmt = (
        select(Mailing)
        .where(Mailing.id.__eq__(id_))
    )
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def get_mailing_messages_by_mailing_id(mailing_id: int, s: AsyncSession = None) -> Sequence[MailingMessage]:
    stmt = (
        select(MailingMessage)
        .where(MailingMessage.mailing_id.__eq__(mailing_id))
    )
    result = await s.execute(stmt)
    return result.scalars().all()


@with_session
async def get_mailing_statistic(mailing_id: int, s: AsyncSession = None) -> dict["MailingMessageStatus", int]:
    stmt = (
        select(
            MailingMessage.status,
            func.count(MailingMessage.id).label('count')
        )
        .where(MailingMessage.mailing_id.__eq__(mailing_id))
        .group_by(MailingMessage.status)
    )
    result = (await s.execute(stmt)).all()
    statistics = {status: count for status, count in result}
    return statistics


@with_session
async def finish_mailing(mailing_id: int, s: AsyncSession = None) -> None:
    try:
        stmt = (
            update(Mailing)
            .where(Mailing.id.__eq__(mailing_id))
            .values(finished_at=now(), status=MailingStatus.COMPLETED)
        )
        await s.execute(stmt)
    except Exception as e:
        logger.error(f"Failed to finish mailing by id: {mailing_id}: {e}")


@with_session
async def get_admin_ids(s: AsyncSession = None) -> ScalarResult[Any]:
    stmt = (select(User.telegram_id)
            .where(User.is_admin.__eq__(True)))
    result = (await s.execute(stmt)).scalars()
    return result


@with_session
async def save_task(task: Task, s: AsyncSession = None) -> None:
    s.add(task)


@with_session(override_name='session')
async def get_active_tasks(session: AsyncSession = None):
    # Subquery to count the number of times each DONE_BASED task has been completed
    done_subquery = (
        select(
            TaskDoneHistory.task_id,
            func.count(TaskDoneHistory.id).label('done_count')
        )
        .group_by(TaskDoneHistory.task_id)
        .subquery()
    )

    # Join the Task table with both subqueries
    stmt = select(Task).outerjoin(
        done_subquery, Task.id == done_subquery.c.task_id
    ).filter(
        or_(
            # Time-based tasks: Not expired or no expiration time set
            and_(
                Task.type == TaskType.TIME_BASED,
                or_(Task.expires_at.is_(None), Task.expires_at > now(native=True))
            ),
            # Subscription-based tasks: done_limit is greater than the count of completed tasks
            and_(
                Task.type == TaskType.DONE_BASED,
                or_(Task.done_limit.is_(None), Task.done_limit > done_subquery.c.done_count)
            ),
            # Pool-based tasks: coin_pool is greater than the sum of distributed rewards
            and_(
                Task.type == TaskType.POOL_BASED,
                or_(Task.coin_pool.is_(None), Task.done_limit > done_subquery.c.done_count)
            )
        )
    )

    result = await session.execute(stmt)
    active_tasks = result.scalars().all()

    return active_tasks


@with_session(override_name='session')
async def get_active_task_by_id(id_: int, session: AsyncSession = None) -> Union[Task, None]:
    # Subquery to count the number of times each DONE_BASED task has been completed
    done_subquery = (
        select(
            TaskDoneHistory.task_id,
            func.count(TaskDoneHistory.id).label('done_count')
        )
        .group_by(TaskDoneHistory.task_id)
        .subquery()
    )

    # Join the Task table with both subqueries
    stmt = select(Task).outerjoin(
        done_subquery, Task.id == done_subquery.c.task_id
    ).filter(
        and_(
            Task.id.__eq__(id_),
            Task.deleted_at.__eq__(None),
            or_(
                # Time-based tasks: Not expired or no expiration time set
                and_(
                    Task.type == TaskType.TIME_BASED,
                    or_(Task.expires_at.is_(None), Task.expires_at > now(native=True))
                ),
                # Subscription-based tasks: done_limit is greater than the count of completed tasks
                and_(
                    Task.type == TaskType.DONE_BASED,
                    or_(Task.done_limit.is_(None), Task.done_limit > done_subquery.c.done_count)
                ),
                # Pool-based tasks: coin_pool is greater than the sum of distributed rewards
                and_(
                    Task.type == TaskType.POOL_BASED,
                    or_(Task.coin_pool.is_(None), Task.done_limit > done_subquery.c.done_count)
                ),
                Task.type == TaskType.BONUS
            )
        )
    )

    result = await session.execute(stmt)
    active_task = result.scalars().one_or_none()

    return active_task


@with_session
async def delete_task_by_id(task_id: int, deleted_by_id: int, s: AsyncSession = None) -> None:
    stmt = (
        update(Task)
        .where(Task.id.__eq__(task_id))
        .values(deleted_at=now(), deleted_by_id=deleted_by_id)
    )
    await s.execute(stmt)
    await s.commit()
    await s.close()


@with_session(override_name='session')
async def get_active_tasks_page(user_id: int,
                                page: int = 1,
                                task_type: TaskType = None,
                                limit: int = 1,
                                session: AsyncSession = None
                                ):
    # Aliasing TaskDoneHistory to join it twice for different purposes
    user_done_history = aliased(TaskDoneHistory)

    # Subquery to count the number of times each DONE_BASED task has been completed
    done_subquery = (
        select(
            TaskDoneHistory.task_id,
            func.count(TaskDoneHistory.id).label('done_count')
        )
        .group_by(TaskDoneHistory.task_id)
        .subquery()
    )

    # Subquery to check if the user has completed each task
    user_done_subquery = (
        select(
            user_done_history.task_id.label('task_id'),
            func.count(user_done_history.id).label('user_done_count')
        )
        .filter(user_done_history.user_id.__eq__(user_id))
        .group_by(user_done_history.task_id)
        .subquery()
    )

    # Build the main query for active tasks
    stmt = (
        select(Task)
        .outerjoin(done_subquery, Task.id == done_subquery.c.task_id)
        .outerjoin(user_done_subquery, Task.id == user_done_subquery.c.task_id)
        .filter(
            and_(
                Task.deleted_at.is_(None),
                or_(
                    # Time-based tasks: Not expired or no expiration time set
                    and_(
                        Task.type == TaskType.TIME_BASED,
                        or_(Task.expires_at.is_(None), Task.expires_at > now(native=True))
                    ),
                    # Subscription-based tasks: done_limit is greater than the count of completed tasks
                    and_(
                        Task.type == TaskType.DONE_BASED,
                        or_(Task.done_limit.is_(None), Task.done_limit > coalesce(done_subquery.c.done_count, 0))
                    ),
                    # Pool-based tasks: coin_pool is greater than the sum of distributed rewards
                    and_(
                        Task.type == TaskType.POOL_BASED,
                        or_(Task.coin_pool.is_(None), Task.coin_pool > coalesce(done_subquery.c.done_count, 0))
                    ),
                    Task.type == TaskType.BONUS
                ),
                or_(
                    # Tasks not done by user
                    user_done_subquery.c.user_done_count.is_(None),
                    user_done_subquery.c.user_done_count == 0
                )
            )
        ).order_by(Task.created_at.desc())  # Order by created_at from new to old
    )

    if task_type is not None:
        stmt = stmt.filter(Task.type.__eq__(task_type))

    # Get the total count of matching tasks asynchronously
    count_stmt = stmt.with_only_columns(func.count()).order_by(None)
    total_tasks = (await session.execute(count_stmt)).scalar()

    # Calculate offset based on the current page number
    offset = (page - 1) * limit

    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    tasks = list(result.scalars().all())

    # Calculate pagination details
    total_pages = (total_tasks + limit - 1) // limit if limit > 0 else 1
    current_page = min(max(page, 1), total_pages)  # Ensure current_page is within the valid range

    return Pagination(
        items=tasks,
        total_items=total_tasks,
        current_page=current_page,
        total_pages=total_pages
    )


@with_session(override_name='session')
async def get_active_task(user_id: int, task_id: int, session: AsyncSession = None):
    # Aliasing TaskDoneHistory to join it twice for different purposes
    user_done_history = aliased(TaskDoneHistory)

    # Subquery to count the number of times each DONE_BASED task has been completed
    done_subquery = (
        select(
            TaskDoneHistory.task_id,
            func.count(TaskDoneHistory.id).label('done_count')
        )
        .group_by(TaskDoneHistory.task_id)
        .subquery()
    )

    # Subquery to check if the user has completed each task
    user_done_subquery = (
        select(
            user_done_history.task_id.label('task_id'),
            func.count(user_done_history.id).label('user_done_count')
        )
        .filter(user_done_history.user_id.__eq__(user_id))
        .group_by(user_done_history.task_id)
        .subquery()
    )

    # Build the main query for active tasks
    stmt = (
        select(Task)
        .outerjoin(done_subquery, Task.id == done_subquery.c.task_id)
        .outerjoin(user_done_subquery, Task.id == user_done_subquery.c.task_id)
        .filter(
            and_(
                Task.deleted_at.is_(None),
                Task.id.__eq__(task_id),
                or_(
                    # Time-based tasks: Not expired or no expiration time set
                    and_(
                        Task.type == TaskType.TIME_BASED,
                        or_(Task.expires_at.is_(None), Task.expires_at > now(native=True))
                    ),
                    # Subscription-based tasks: done_limit is greater than the count of completed tasks
                    and_(
                        Task.type == TaskType.DONE_BASED,
                        or_(Task.done_limit.is_(None), Task.done_limit > coalesce(done_subquery.c.done_count, 0))
                    ),
                    # Pool-based tasks: coin_pool is greater than the sum of distributed rewards
                    and_(
                        Task.type == TaskType.POOL_BASED,
                        or_(Task.coin_pool.is_(None), Task.coin_pool > coalesce(done_subquery.c.done_count, 0))
                    ),
                    Task.type == TaskType.BONUS
                ),
                or_(
                    # Tasks not done by user
                    user_done_subquery.c.user_done_count.is_(None),
                    user_done_subquery.c.user_done_count == 0
                )
            )
        ).order_by(Task.created_at.desc())  # Order by created_at from new to old
    )

    result = await session.execute(stmt)
    active_task = result.scalars().one_or_none()

    return active_task


@with_session
async def get_tasks_statistics(s: AsyncSession = None):
    stmt = (
        select(
            Task.id,
            func.count(TaskDoneHistory.id).label('done_count'),
        )
        .join(TaskDoneHistory, TaskDoneHistory.task_id == Task.id)
        .where(Task.expires_at > func.now())
        .where(Task.deleted_at.is_(None))
        .group_by(Task.id)
        .order_by(Task.id.desc())
    )

    result = await s.execute(stmt)
    return result.all()


@with_session
async def get_task_statistic(id_: int, s: AsyncSession = None):
    stmt = (
        select(
            Task,
            func.count(TaskDoneHistory.id).label('done_count')
        )
        .join(TaskDoneHistory, TaskDoneHistory.task_id == Task.id)
        .where(Task.id.__eq__(id_))
        .group_by(Task.id)
    )

    result = await s.execute(stmt)
    return result.one_or_none()


@with_session
async def check_task_is_done(task_id: int, user_id: int, s: AsyncSession = None) -> bool:
    stmt = (
        select(TaskDoneHistory)
        .where(and_(TaskDoneHistory.task_id.__eq__(task_id),
                    TaskDoneHistory.user_id.__eq__(user_id)))
        .exists()
        .select()
    )
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def save_activity_statistic(user_id: int, context: UserActivityContext, s: AsyncSession = None) -> None:
    statistic = UserActivityStatistic(
        user_id=user_id,
        context=context
    )
    s.add(statistic)


@with_session
async def get_user_activity_statistic(s: AsyncSession = None):
    stmt = select(UserActivityStatistic).limit(1)
    result = await s.execute(stmt)
    return result.scalar()


@cache.cacheable(ttl="10m")
@with_session
async def is_client_token_valid(id_: str, type_: CustomClientTokenType, s: AsyncSession = None) -> bool:
    stmt = (select(CustomClientToken)
            .where(and_(CustomClientToken.deleted_at.is_(None),
                        CustomClientToken.id.__eq__(id_),
                        CustomClientToken.type.__eq__(type_)))
            .exists()
            .select()
            )
    result = await s.execute(stmt)
    return result.scalar()


@with_session
async def get_active_cheque_by_id(id_: int, s: AsyncSession = None) -> Optional[Cheque]:
    # Subquery to count the number of activations for the given cheque
    activation_count_subquery = (
        select(func.count(ChequeActivation.id))
        .where(ChequeActivation.cheque_id == Cheque.id)
        .scalar_subquery()
    )

    # Main query to get the cheque and filter based on the activation count
    stmt = (
        select(Cheque)
        .where(and_(
            Cheque.id == id_,
            Cheque.deleted_at.is_(None),
            activation_count_subquery < Cheque.activation_limit
        ))
    )

    result = await s.execute(stmt)
    return result.scalar_one_or_none()