from applications.purchases.models import Purchase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


async def get_user_purchases(user_id: int, session: AsyncSession):
    result = await session.execute(
        select(Purchase)
        .options(joinedload(Purchase.product))
        .filter(Purchase.user_id == user_id)
        .order_by(Purchase.created_at.desc())
    )
    return result.scalars().all()
