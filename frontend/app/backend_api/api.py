import httpx
from settings import settings
from fastapi import Request


async def add_product_to_cart(access_token: str, product_id: int):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}cart/add/{product_id}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


async def remove_product_from_cart(access_token: str, product_id: int):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}cart/remove/{product_id}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


async def get_cart_products(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.BACKEND_API}cart",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()


async def login_user(user_email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}auth/login",
            data={"username": user_email, "password": password},
        )
        return response.json()


async def register_user(user_email: str, password: str, name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{settings.BACKEND_API}users/create",
            json={"name": name, "password": password, "email": user_email},
            headers={"Content-Type": "application/json"},
        )
        return response.json()


async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.BACKEND_API}auth/get-my-info",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.json()


async def get_current_user_with_token(request: Request) -> dict:
    access_token = request.cookies.get("access_token")
    if not access_token:
        return {}
    user = await get_user_info(access_token)
    user["access_token"] = access_token
    return user


async def get_products(q: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.BACKEND_API}products/", params={"q": q}
        )
        return response.json()


async def get_product(pk: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.BACKEND_API}products/{pk}",
        )
        return response.json()
