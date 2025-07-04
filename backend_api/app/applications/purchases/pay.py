from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from applications.users.models import User
from applications.purchases.models import Purchase
from applications.products.models import CartProduct
from applications.auth.security import get_current_user
from database.session_dependencies import get_async_session
import sqlalchemy as sa
from datetime import datetime


pay_router = APIRouter()

@pay_router.post("/pay")
async def pay_for_cart(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):

    cart_products = await session.execute(
        sa.select(CartProduct).where(CartProduct.cart.has(user_id=current_user.id))
    )
    cart_products = cart_products.scalars().all()

    if not cart_products:
        raise HTTPException(status_code=400, detail="Cart is empty")
    for cp in cart_products:
        purchase = Purchase(
            user_id=current_user.id,
            product_id=cp.product_id,
            created_at=datetime.utcnow(),
        )
        session.add(purchase)
    await session.execute(
        sa.delete(CartProduct).where(CartProduct.cart.has(user_id=current_user.id))
    )

    await session.commit()
    return {"detail": "Payment successful, purchases added to your library"}
