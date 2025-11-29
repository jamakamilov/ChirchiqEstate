from database import AsyncSessionLocal
from models.analytics import ViewStat
from sqlalchemy import select, func

async def record_view(listing_id: int, user_id: int = None, action: str = "view"):
    async with AsyncSessionLocal() as session:
        stat = ViewStat(listing_id=listing_id, user_id=user_id, action=action)
        session.add(stat)
        await session.commit()
        await session.refresh(stat)
        return stat

async def popular_regions(limit=10):
    async with AsyncSessionLocal() as session:
        q = await session.execute(
            select(ViewStat).limit(limit)
        )
        return q.scalars().all()
