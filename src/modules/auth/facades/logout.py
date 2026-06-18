from fastapi import status
from fastapi.responses import Response


async def logout() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
