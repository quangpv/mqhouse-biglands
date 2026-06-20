from fastapi import APIRouter

from src.modules.auth.router import router


def module():
    return router
