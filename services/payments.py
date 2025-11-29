from database import AsyncSessionLocal
from models.payments import Payment
from models.user import User
from utils.logger import logger
from sqlalchemy import select, update

async def create_payment(user_id: int, role_id: int, amount: float, screenshot: str = None):
    async with AsyncSessionLocal() as session:
        p = Payment(user_id=user_id, role_id=role_id, amount=amount, screenshot=screenshot)
        session.add(p)
        await session.commit()
        await session.refresh(p)
        logger.info(f"Payment created {p.id}")
        return p

async def list_pending():
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(Payment).where(Payment.status == "pending"))
        return q.scalars().all()

async def set_payment_status(payment_id: int, status: str):
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(Payment).where(Payment.id == payment_id))
        p = q.scalar_one_or_none()
        if not p:
            return None
        p.status = status
        await session.commit()
        await session.refresh(p)
        return p
