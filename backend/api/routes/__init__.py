"""
API route definitions for the workflow automation system.
"""

from fastapi import APIRouter

router = APIRouter()

# Import all route modules here
# Import all route modules here
from .workflow_routes import router as workflow_router
from .user_routes import router as user_router
from .execution_routes import router as execution_router

# Include all routers
router.include_router(workflow_router, prefix="/workflows", tags=["workflows"])
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(execution_router, prefix="/execute", tags=["execution"]) 