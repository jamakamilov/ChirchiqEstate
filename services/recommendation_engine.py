from database import AsyncSessionLocal
from models.listing import Listing
from sqlalchemy import select, and_
import statistics

async def similar_listings(listing: Listing, limit=5):
    async with AsyncSessionLocal() as session:
        q = select(Listing).where(
            Listing.status == "published",
            Listing.region == listing.region,
            Listing.deal_type == listing.deal_type
        ).limit(limit)
        res = await session.execute(q)
        return res.scalars().all()

async def avg_price_by_region(region: str):
    async with AsyncSessionLocal() as session:
        q = select(Listing.price).where(Listing.region == region, Listing.price != None)
        res = await session.execute(q)
        prices = [r[0] for r in res.all()]
        if not prices:
            return None
        return statistics.mean(prices)
