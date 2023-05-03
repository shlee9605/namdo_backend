from models import postgresql
# from libs.scheduleUtil import scheduler

async def on_app_start():
    await postgresql.connect()
    # await scheduler.start()

async def on_app_shutdown():
    await postgresql.close()
    # scheduler.stop()
