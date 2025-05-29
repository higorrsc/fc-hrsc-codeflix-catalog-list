from fastapi import FastAPI

from src.infra.api.http.router.cast_member import router as cast_member_router
from src.infra.api.http.router.category import router as category_router

app = FastAPI()
app.include_router(router=category_router, prefix="/categories")
app.include_router(router=cast_member_router, prefix="/cast_members")


@app.get("/healthcheck")
def healthcheck():
    """
    Simple healthcheck endpoint that returns a static ok status.

    This endpoint does not do any actual health checking on the service
    or its dependencies. It is intended to be used by load balancers
    or other infrastructure to quickly check the health of the service.

    Returns:
        dict: A dictionary containing a status key with value 200.
    """

    return {"status": 200}
