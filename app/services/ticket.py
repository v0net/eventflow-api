from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.models.ticket import Ticket


class TicketService:
    @staticmethod
    async def get_by_id(session: AsyncSession, ticket_id: int) -> Ticket | None:
        stmt = select(Ticket).where(Ticket.id == ticket_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_tickets(
        session: AsyncSession, user_id: int
    ) -> list[Ticket]:
        stmt = select(Ticket).where(Ticket.user_id == user_id)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def book_ticket(
        session: AsyncSession, event_id: int, user_id: int
    ) -> Ticket:
        event_stmt = select(Event).where(Event.id == event_id)
        event_res = await session.execute(event_stmt)
        event = event_res.scalar_one_or_none()
        if not event:
            raise ValueError("Event not found")

        existing_stmt = select(Ticket).where(
            Ticket.event_id == event_id, Ticket.user_id == user_id
        )
        existing_res = await session.execute(existing_stmt)
        if existing_res.scalar_one_or_none():
            raise ValueError("You have already booked a ticket for this event")

        count_stmt = select(func.count(Ticket.id)).where(Ticket.event_id == event_id)
        count_res = await session.execute(count_stmt)
        booked_seats = count_res.scalar_one()

        if booked_seats >= event.total_seats:
            raise ValueError("All seats for this event are already booked")

        ticket = Ticket(event_id=event_id, user_id=user_id)
        session.add(ticket)
        await session.flush()
        await session.refresh(ticket)
        return ticket

    @staticmethod
    async def cancel_ticket(session: AsyncSession, ticket: Ticket) -> None:
        await session.delete(ticket)