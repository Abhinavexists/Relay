import httpx
import logging
from typing import List, Dict, Any, Optional
from ..config import settings

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = f"http://{settings.API_HOST}:{settings.API_PORT}/api"
        self.client = httpx.AsyncClient(timeout=30.0)
        self.tokens: Dict[str, str] = {}  # user_id -> token mapping

    async def close(self):
        await self.client.aclose()

    async def register_user(self, telegram_id: str, email: str, password: str, full_name: str) -> Dict[str, Any]:
        """Register a new user."""
        try:
            response = await self.client.post(
                f"{self.base_url}/users/register",
                json={
                    "email": email,
                    "password": password,
                    "full_name": full_name
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            raise

    async def login_user(self, telegram_id: str, email: str, password: str) -> str:
        """Login user and store token."""
        try:
            response = await self.client.post(
                f"{self.base_url}/users/login",
                data={
                    "username": email,
                    "password": password
                }
            )
            response.raise_for_status()
            token_data = response.json()
            token = token_data["access_token"]
            self.tokens[telegram_id] = token
            return token
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            raise

    def _get_headers(self, telegram_id: str) -> Dict[str, str]:
        """Get authorization headers for a user."""
        token = self.tokens.get(telegram_id)
        if not token:
            raise ValueError("User not authenticated. Please login first.")
        return {"Authorization": f"Bearer {token}"}

    async def get_user_workflows(self, telegram_id: str) -> List[Dict[str, Any]]:
        """Get all workflows for a user."""
        try:
            headers = self._get_headers(telegram_id)
            response = await self.client.get(
                f"{self.base_url}/workflows",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting workflows: {e}")
            raise

    async def generate_workflow(self, telegram_id: str, description: str) -> Dict[str, Any]:
        """Generate a workflow from natural language description."""
        try:
            headers = self._get_headers(telegram_id)
            response = await self.client.post(
                f"{self.base_url}/workflows/generate",
                headers=headers,
                json={"description": description}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error generating workflow: {e}")
            raise

    async def get_workflow(self, telegram_id: str, workflow_id: str) -> Dict[str, Any]:
        """Get a specific workflow by ID."""
        try:
            headers = self._get_headers(telegram_id)
            response = await self.client.get(
                f"{self.base_url}/workflows/{workflow_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting workflow: {e}")
            raise

    async def execute_workflow(self, telegram_id: str, workflow_id: str, input_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a workflow."""
        try:
            headers = self._get_headers(telegram_id)
            response = await self.client.post(
                f"{self.base_url}/execute/{workflow_id}",
                headers=headers,
                json=input_data or {}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            raise

    async def get_execution_status(self, telegram_id: str, execution_id: str) -> Dict[str, Any]:
        """Get execution status."""
        try:
            headers = self._get_headers(telegram_id)
            response = await self.client.get(
                f"{self.base_url}/execute/{execution_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting execution status: {e}")
            raise

    async def delete_workflow(self, telegram_id: str, workflow_id: str) -> None:
        """Delete a workflow."""
        try:
            headers = self._get_headers(telegram_id)
            response = await self.client.delete(
                f"{self.base_url}/workflows/{workflow_id}",
                headers=headers
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error deleting workflow: {e}")
            raise

# Create a singleton instance
api_client = APIClient()

# Export functions for easy access
async def register_user(telegram_id: str, email: str, password: str, full_name: str) -> Dict[str, Any]:
    return await api_client.register_user(telegram_id, email, password, full_name)

async def login_user(telegram_id: str, email: str, password: str) -> str:
    return await api_client.login_user(telegram_id, email, password)

async def get_user_workflows(telegram_id: str) -> List[Dict[str, Any]]:
    return await api_client.get_user_workflows(telegram_id)

async def generate_workflow(telegram_id: str, description: str) -> Dict[str, Any]:
    return await api_client.generate_workflow(telegram_id, description)

async def get_workflow(telegram_id: str, workflow_id: str) -> Dict[str, Any]:
    return await api_client.get_workflow(telegram_id, workflow_id)

async def execute_workflow(telegram_id: str, workflow_id: str, input_data: Optional[Dict] = None) -> Dict[str, Any]:
    return await api_client.execute_workflow(telegram_id, workflow_id, input_data)

async def get_execution_status(telegram_id: str, execution_id: str) -> Dict[str, Any]:
    return await api_client.get_execution_status(telegram_id, execution_id)

async def delete_workflow(telegram_id: str, workflow_id: str) -> None:
    await api_client.delete_workflow(telegram_id, workflow_id)
