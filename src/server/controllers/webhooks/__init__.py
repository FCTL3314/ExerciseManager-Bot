from fastapi import APIRouter

router = APIRouter()

from src.server.controllers.webhooks.telegram import *
