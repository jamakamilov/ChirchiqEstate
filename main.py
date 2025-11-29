import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from utils.logger import logger
from database import init_db
from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.roles import router as roles_router
from handlers.create_listing.step1_type import router as cl_step1
from handlers.create_listing.step2_location import router as cl_step2
from handlers.create_listing.step3_price import router as cl_step3
from handlers.create_listing.step4_details import router as cl_step4
from handlers.create_listing.step5_photos import router as cl_step5
from handlers.create_listing.finish import router as cl_finish
from handlers.search import router as search_router
from handlers.favorites import router as fav_router
from handlers.recommendations import router as rec_router
from handlers.deal import router as deal_router
from admin.mod_listings import router as admin_mod_listings
from admin.mod_payments import router as admin_mod_payments
from admin.mod_commissions import router as admin_mod_commissions
from admin.admin_stats import router as admin_stats
from admin.admin_roles import router as admin_roles
from aiogram import types

async def main():
    await init_db()
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # include routers
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(roles_router)
    dp.include_router(cl_step1)
    dp.include_router(cl_step2)
    dp.include_router(cl_step3)
    dp.include_router(cl_step4)
    dp.include_router(cl_step5)
    dp.include_router(cl_finish)
    dp.include_router(search_router)
    dp.include_router(fav_router)
    dp.include_router(rec_router)
    dp.include_router(deal_router)
    dp.include_router(admin_mod_listings)
    dp.include_router(admin_mod_payments)
    dp.include_router(admin_mod_commissions)
    dp.include_router(admin_stats)
    dp.include_router(admin_roles)

    # simple command handlers
    @dp.message(commands=["help"])
    async def help_cmd(message: types.Message):
        await message.answer("Help: /start")

    logger.info("Bot starting...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
