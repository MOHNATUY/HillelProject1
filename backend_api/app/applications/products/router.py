import uuid
from typing import Annotated

from applications.auth.security import admin_required, get_current_user
from applications.products.crud import (
    create_product_in_db,
    get_or_create_cart,
    get_or_create_cart_product,
    get_product_by_pk,
    get_products_data,
)
from applications.products.schemas import CartSchema, ProductSchema, SearchParamsSchema
from applications.users.models import User
from database.session_dependencies import get_async_session
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status
from services.s3.s3 import s3_storage
from sqlalchemy.ext.asyncio import AsyncSession

products_router = APIRouter()
cart_router = APIRouter()


@cart_router.get("/")
async def get_current_cart(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CartSchema:
    cart = await get_or_create_cart(user_id=user.id, session=session)
    return cart


@cart_router.patch("/change-products")
async def change_products(
    quantity: float,
    product_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CartSchema:
    cart = await get_or_create_cart(user_id=user.id, session=session)
    product = await get_product_by_pk(product_id, session)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No product"
        )

    cart_product = await get_or_create_cart_product(product_id, cart.id, session)

    new_quantity = cart_product.quantity + quantity

    if new_quantity <= 0:
        await session.delete(cart_product)
    else:
        cart_product.quantity = new_quantity
        cart_product.price = product.price
        session.add(cart_product)

    await session.commit()
    await session.refresh(cart)

    return cart


@products_router.post("/", dependencies=[Depends(admin_required)])
async def create_product(
    main_image: UploadFile,
    images: list[UploadFile] = None,
    title: str = Body(max_length=100),
    description: str = Body(max_length=1000),
    price: float = Body(gt=1),
    session: AsyncSession = Depends(get_async_session),
) -> ProductSchema:
    product_uuid = uuid.uuid4()
    main_image = await s3_storage.upload_product_image(
        main_image, product_uuid=product_uuid
    )
    images = images or []
    images_urls = []
    for image in images:
        url = await s3_storage.upload_product_image(image, product_uuid=product_uuid)
        images_urls.append(url)

    created_product = await create_product_in_db(
        product_uuid=product_uuid,
        title=title,
        description=description,
        price=price,
        main_image=main_image,
        images=images_urls,
        session=session,
    )
    return created_product


@products_router.get("/{pk}")
async def get_product(
    pk: int,
    session: AsyncSession = Depends(get_async_session),
) -> ProductSchema:
    product = await get_product_by_pk(pk, session)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with pk #{pk} not found",
        )
    return product


@products_router.get("/")
async def get_products(
    params: Annotated[SearchParamsSchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    result = await get_products_data(params, session)
    return result
