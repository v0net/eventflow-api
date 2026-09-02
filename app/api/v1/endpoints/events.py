from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.event import EventCreate, EventRead
from app.services.event import EventService

router = APIRouter()


@router.post(
    "/",
    response_model=EventRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create event",
)
async def create_event(
    event_in: EventCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    return await EventService.create(session, event_in, owner_id=current_user.id)


@router.get(
    "/",
    response_model=list[EventRead],
    summary="List events with pagination",
)
async def list_events(
    session: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(default=0, ge=0, description="Skip count / offset"),
    limit: int = Query(default=20, ge=1, le=100, description="Items limit per page"),
):
    return await EventService.get_multi(session, skip=skip, limit=limit)


@router.get(
    "/{event_id}",
    response_model=EventRead,
    summary="Get event by ID",
)
async def get_event(
    event_id: int,
    session: Annotated[AsyncSession, Depends(get_db)],
):
    event = await EventService.get_by_id(session, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete event",
)
async def delete_event(
    event_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_db)],
):
    event = await EventService.get_by_id(session, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    if event.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this event",
        )
    await EventService.delete(session, event)