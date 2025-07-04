from applications.auth.security import get_current_user
from applications.purchases.crud import get_user_purchases
from applications.purchases.schemas import PurchaseSchema
from applications.users.models import User
from database.session_dependencies import get_async_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

purchases_router = APIRouter()


@purchases_router.get("/my-purchases", response_model=list[PurchaseSchema])
async def get_my_purchases(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    purchases = await get_user_purchases(user.id, session)
    return [
        {
            "product": {
                "id": p.product.id,
                "title": p.product.title,
                "price": p.product.price,
                "main_image": p.product.main_image,
            },
            "created_at": p.created_at.isoformat(),
        }
        for p in purchases
    ]
