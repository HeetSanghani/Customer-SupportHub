from fastapi import APIRouter
from app.routers.webhooks.email import router as email_router
from app.routers.webhooks.whatsapp import router as whatsapp_router
from app.routers.webhooks.messenger import router as messenger_router

router = APIRouter(prefix="/webhooks")

router.include_router(email_router)
router.include_router(whatsapp_router)
router.include_router(messenger_router)
