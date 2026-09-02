from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.event import Event
from app.schemas.event import EventCreate


class EventService:
    @staticmethod
    async def get_by_id(session: AsyncSession, event_id: int) -> Event | None:
        stmt = (
            select(Event)
            .options(joinedload(Event.owner))
            .where(Event.id == event_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_multi(
        session: AsyncSession, skip: int = 0, limit: int = 20
    ) -> list[Event]:
        stmt = (
            select(Event)
            .options(joinedload(Event.owner))
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def create(
        session: AsyncSession, event_in: EventCreate, owner_id: int
    ) -> Event:
        event = Event(**event_in.model_dump(), owner_id=owner_id)
        session.add(event)
        await session.flush()
        await session.refresh(event)
        return event

    @staticmethod
    async def delete(session: AsyncSession, event: Event) -> None:
        await session.delete(event)