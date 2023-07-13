from fastapi import APIRouter

from routes import auth, user
from routes import plan, process, facility, bom, gant, achievement, dashboard

router = APIRouter()

# router config
router.include_router(plan.router)
router.include_router(process.router)
router.include_router(facility.router)
router.include_router(bom.router)
router.include_router(gant.router)
router.include_router(achievement.router)
router.include_router(dashboard.router)

router.include_router(auth.router)
router.include_router(user.router)



