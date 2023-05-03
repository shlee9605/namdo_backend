from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from models import mongodb
from models.users import Users

class Scheduler:
    def __init__(self):
        self.sched = AsyncIOScheduler(timezone="Asia/Seoul")

    async def scheduled_job(self):
        # Hard-Delete Outdated Data
        num = await mongodb.engine.remove(Users, Users.deletedAt != None)
        print(f"{num} Deleted, Scheduled job is running {datetime.now(timezone('Asia/Seoul'))}")

    async def start(self):
        await self.scheduled_job()
        self.sched.add_job(self.scheduled_job, 'cron', day_of_week='sun', hour=21, minute=00, second=30)
        self.sched.start()

    def stop(self):
        self.sched.shutdown()

scheduler = Scheduler()
