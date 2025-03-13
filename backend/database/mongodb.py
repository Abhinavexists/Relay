from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client = None
    db = None

db = Database()

async def init_db():
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.MONGODB_DB_NAME]
    logger.info("Connected to MongoDB.")
    
    # Create collections if they don't exist
    try:
        await db.db.command({"listCollections": 1})
        if "users" not in await db.db.list_collection_names():
            await db.db.create_collection("users")
        if "workflows" not in await db.db.list_collection_names():
            await db.db.create_collection("workflows")
        if "workflow_executions" not in await db.db.list_collection_names():
            await db.db.create_collection("workflow_executions")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

async def close_db():
    if db.client:
        logger.info("Closing MongoDB connection...")
        db.client.close()
        logger.info("MongoDB connection closed.")

# User collection operations
async def get_user_by_email(email: str):
    return await db.db.users.find_one({"email": email})

async def get_user_by_id(user_id: str):
    return await db.db.users.find_one({"id": user_id})

async def create_user(user_data: dict):
    user = await db.db.users.insert_one(user_data)
    return user

async def update_user(user_id: str, user_data: dict):
    result = await db.db.users.update_one(
        {"id": user_id},
        {"$set": user_data}
    )
    return result.modified_count > 0

# Workflow collection operations
async def create_workflow(workflow_data: dict):
    result = await db.db.workflows.insert_one(workflow_data)
    return result.inserted_id

async def get_workflow(workflow_id: str):
    return await db.db.workflows.find_one({"id": workflow_id})

async def get_workflows_by_user(user_id: str, skip: int = 0, limit: int = 100):
    cursor = db.db.workflows.find({"created_by": user_id}).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def update_workflow(workflow_id: str, workflow_data: dict):
    result = await db.db.workflows.update_one(
        {"id": workflow_id},
        {"$set": workflow_data}
    )
    return result.modified_count > 0

async def delete_workflow(workflow_id: str):
    result = await db.db.workflows.delete_one({"id": workflow_id})
    return result.deleted_count > 0

# Workflow execution operations
async def create_execution(execution_data: dict):
    result = await db.db.workflow_executions.insert_one(execution_data)
    return result.inserted_id

async def get_execution(execution_id: str):
    return await db.db.workflow_executions.find_one({"id": execution_id})

async def get_executions_by_workflow(workflow_id: str, skip: int = 0, limit: int = 100):
    cursor = db.db.workflow_executions.find({"workflow_id": workflow_id}).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def update_execution(execution_id: str, execution_data: dict):
    result = await db.db.workflow_executions.update_one(
        {"id": execution_id},
        {"$set": execution_data}
    )
    return result.modified_count > 0